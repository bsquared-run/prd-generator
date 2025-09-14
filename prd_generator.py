import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import re
import json
import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

@dataclass
class UserStory:
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: str = "Medium"
    story_points: Optional[int] = None

@dataclass
class PRDSection:
    title: str
    content: str

class UserStoryParser:
    def __init__(self):
        self.story_patterns = {
            'gherkin': r'As a (.+?), I want (.+?) so that (.+?)(?:\.|$)',
            'simple': r'(.+?)(?:\n|$)',
            'acceptance': r'(?:Given|When|Then|And)\s+(.+?)(?:\n|$)',
            'criteria': r'(?:Acceptance Criteria?:|AC:)\s*\n?((?:.+\n?)*)',
            'priority': r'(?:Priority:|Prio:)\s*(\w+)',
            'points': r'(?:Story Points?:|Points?:|SP:)\s*(\d+)'
        }

    def parse_user_stories(self, text: str) -> List[UserStory]:
        stories = []
        story_blocks = self._split_into_stories(text)

        for block in story_blocks:
            story = self._parse_single_story(block)
            if story:
                stories.append(story)

        return stories

    def _split_into_stories(self, text: str) -> List[str]:
        lines = text.strip().split('\n')
        current_story = []
        stories = []

        for line in lines:
            line = line.strip()
            if not line:
                if current_story:
                    stories.append('\n'.join(current_story))
                    current_story = []
            else:
                current_story.append(line)

        if current_story:
            stories.append('\n'.join(current_story))

        return stories

    def _parse_single_story(self, text: str) -> Optional[UserStory]:
        title = ""
        description = ""
        acceptance_criteria = []
        priority = "Medium"
        story_points = None

        gherkin_match = re.search(self.story_patterns['gherkin'], text, re.IGNORECASE)
        if gherkin_match:
            persona, action, benefit = gherkin_match.groups()
            title = f"User Story: {action}"
            description = f"As a {persona}, I want {action} so that {benefit}"
        else:
            lines = text.split('\n')
            if lines:
                title = lines[0][:100] + "..." if len(lines[0]) > 100 else lines[0]
                description = text

        criteria_match = re.search(self.story_patterns['criteria'], text, re.IGNORECASE | re.DOTALL)
        if criteria_match:
            criteria_text = criteria_match.group(1)
            acceptance_criteria = [ac.strip() for ac in criteria_text.split('\n') if ac.strip()]

        acceptance_matches = re.findall(self.story_patterns['acceptance'], text, re.IGNORECASE)
        acceptance_criteria.extend(acceptance_matches)

        priority_match = re.search(self.story_patterns['priority'], text, re.IGNORECASE)
        if priority_match:
            priority = priority_match.group(1).capitalize()

        points_match = re.search(self.story_patterns['points'], text, re.IGNORECASE)
        if points_match:
            story_points = int(points_match.group(1))

        if title and description:
            return UserStory(
                title=title,
                description=description,
                acceptance_criteria=acceptance_criteria,
                priority=priority,
                story_points=story_points
            )

        return None

class PRDGenerator:
    def __init__(self):
        self.template = {
            "project_info": {
                "title": "",
                "author": "",
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "version": "1.0",
                "status": "Draft"
            },
            "sections": [
                "Executive Summary",
                "Product Overview",
                "Market Assessment",
                "User Stories and Requirements",
                "Functional Requirements",
                "Technical Requirements",
                "User Experience Requirements",
                "Assumptions and Constraints",
                "Success Metrics",
                "Timeline and Milestones",
                "Appendices"
            ]
        }

    def generate_prd(self, user_stories: List[UserStory], project_info: Dict) -> List[PRDSection]:
        sections = []

        sections.append(PRDSection("Project Information", self._generate_project_info(project_info)))
        sections.append(PRDSection("Executive Summary", self._generate_executive_summary(user_stories, project_info)))
        sections.append(PRDSection("Product Overview", self._generate_product_overview(project_info)))
        sections.append(PRDSection("User Stories and Requirements", self._generate_user_stories_section(user_stories)))
        sections.append(PRDSection("Functional Requirements", self._generate_functional_requirements(user_stories)))
        sections.append(PRDSection("Acceptance Criteria", self._generate_acceptance_criteria(user_stories)))
        sections.append(PRDSection("Assumptions and Constraints", self._generate_assumptions()))
        sections.append(PRDSection("Success Metrics", self._generate_success_metrics()))

        return sections

    def _generate_project_info(self, project_info: Dict) -> str:
        return f"""
Project Title: {project_info.get('title', 'Untitled Project')}
Author: {project_info.get('author', 'Unknown')}
Date: {project_info.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))}
Version: {project_info.get('version', '1.0')}
Status: {project_info.get('status', 'Draft')}
Target Release: {project_info.get('target_release', 'TBD')}
        """.strip()

    def _generate_executive_summary(self, user_stories: List[UserStory], project_info: Dict) -> str:
        total_stories = len(user_stories)
        high_priority = len([s for s in user_stories if s.priority.lower() == 'high'])

        return f"""
This Product Requirements Document outlines the requirements for {project_info.get('title', 'the project')}.

The product addresses key user needs through {total_stories} user stories, with {high_priority} high-priority features identified. This document serves as the primary reference for development teams, stakeholders, and project managers throughout the product development lifecycle.

Key objectives:
- Deliver user-centered features based on identified user stories
- Ensure clear requirements and acceptance criteria
- Provide measurable success metrics
- Establish development timeline and constraints
        """.strip()

    def _generate_product_overview(self, project_info: Dict) -> str:
        return f"""
Product Vision: {project_info.get('vision', 'To be defined based on user requirements')}

Target Users: Based on the user stories, the primary users include various personas who require the functionality described in the requirements.

Core Value Proposition: The product will deliver value by addressing specific user needs as outlined in the user stories section.

Scope: This PRD covers the features and functionality derived from the provided user stories and their associated acceptance criteria.
        """.strip()

    def _generate_user_stories_section(self, user_stories: List[UserStory]) -> str:
        content = "The following user stories define the core requirements for this product:\n\n"

        for i, story in enumerate(user_stories, 1):
            content += f"US{i:03d}: {story.title}\n"
            content += f"Description: {story.description}\n"
            content += f"Priority: {story.priority}\n"
            if story.story_points:
                content += f"Story Points: {story.story_points}\n"
            content += "\n"

        return content.strip()

    def _generate_functional_requirements(self, user_stories: List[UserStory]) -> str:
        content = "Based on the user stories, the following functional requirements have been identified:\n\n"

        for i, story in enumerate(user_stories, 1):
            content += f"FR{i:03d}: {story.title}\n"
            content += f"The system shall implement functionality to: {story.description}\n"
            content += f"Priority Level: {story.priority}\n\n"

        return content.strip()

    def _generate_acceptance_criteria(self, user_stories: List[UserStory]) -> str:
        content = "Acceptance criteria for each user story:\n\n"

        for i, story in enumerate(user_stories, 1):
            if story.acceptance_criteria:
                content += f"US{i:03d} - {story.title}:\n"
                for j, criteria in enumerate(story.acceptance_criteria, 1):
                    content += f"  AC{i:03d}.{j}: {criteria}\n"
                content += "\n"

        return content.strip()

    def _generate_assumptions(self) -> str:
        return """
The following assumptions are made for this product development:

1. Technical infrastructure and development resources are available
2. User stories represent validated user needs
3. Acceptance criteria are complete and testable
4. Dependencies with external systems are manageable
5. Timeline estimates are based on standard development practices

These assumptions should be validated and updated as the project progresses.
        """.strip()

    def _generate_success_metrics(self) -> str:
        return """
Success will be measured using the following metrics:

1. Feature Completion Rate: Percentage of user stories successfully implemented
2. Acceptance Criteria Pass Rate: Percentage of acceptance criteria met
3. User Satisfaction: To be measured through user feedback and testing
4. Performance Metrics: Response time, uptime, and system reliability
5. Adoption Metrics: User engagement and feature utilization

Specific targets and measurement methods should be defined during the planning phase.
        """.strip()

class PRDGeneratorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PRD Generator - User Story to Product Requirements")
        self.root.geometry("1400x900")

        self.parser = UserStoryParser()
        self.generator = PRDGenerator()
        self.current_stories = []
        self.current_prd = []

        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(
            main_frame,
            text="PRD Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.setup_left_panel(content_frame)
        self.setup_right_panel(content_frame)
        self.setup_bottom_panel(main_frame)

    def setup_left_panel(self, parent):
        left_frame = ctk.CTkFrame(parent)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        input_label = ctk.CTkLabel(
            left_frame,
            text="User Stories Input",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_label.pack(pady=(10, 5))

        help_text = ctk.CTkLabel(
            left_frame,
            text="Enter user stories (one per paragraph). Supports Gherkin format and acceptance criteria.",
            font=ctk.CTkFont(size=12)
        )
        help_text.pack(pady=(0, 10))

        self.input_text = ctk.CTkTextbox(
            left_frame,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.input_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.parse_button = ctk.CTkButton(
            button_frame,
            text="Parse User Stories",
            command=self.parse_stories,
            font=ctk.CTkFont(weight="bold")
        )
        self.parse_button.pack(side="left", padx=(0, 5))

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_input
        )
        self.clear_button.pack(side="left", padx=5)

        self.load_button = ctk.CTkButton(
            button_frame,
            text="Load File",
            command=self.load_file
        )
        self.load_button.pack(side="right")

        self.project_info_frame = ctk.CTkFrame(left_frame)
        self.project_info_frame.pack(fill="x", padx=10, pady=(0, 10))

        info_label = ctk.CTkLabel(
            self.project_info_frame,
            text="Project Information",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_label.pack(pady=(10, 5))

        self.project_title = ctk.CTkEntry(
            self.project_info_frame,
            placeholder_text="Project Title"
        )
        self.project_title.pack(fill="x", padx=10, pady=2)

        self.project_author = ctk.CTkEntry(
            self.project_info_frame,
            placeholder_text="Author Name"
        )
        self.project_author.pack(fill="x", padx=10, pady=2)

        self.target_release = ctk.CTkEntry(
            self.project_info_frame,
            placeholder_text="Target Release Date"
        )
        self.target_release.pack(fill="x", padx=10, pady=(2, 10))

    def setup_right_panel(self, parent):
        right_frame = ctk.CTkFrame(parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        output_label = ctk.CTkLabel(
            right_frame,
            text="Generated PRD",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        output_label.pack(pady=(10, 5))

        self.output_text = ctk.CTkTextbox(
            right_frame,
            height=500,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_bottom_panel(self, parent):
        bottom_frame = ctk.CTkFrame(parent)
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.generate_button = ctk.CTkButton(
            bottom_frame,
            text="Generate PRD",
            command=self.generate_prd,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.generate_button.pack(side="left", padx=(10, 5), pady=10)

        self.export_pdf_button = ctk.CTkButton(
            bottom_frame,
            text="Export as PDF",
            command=self.export_pdf,
            height=40
        )
        self.export_pdf_button.pack(side="left", padx=5, pady=10)

        self.export_txt_button = ctk.CTkButton(
            bottom_frame,
            text="Export as Text",
            command=self.export_text,
            height=40
        )
        self.export_txt_button.pack(side="left", padx=5, pady=10)

        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="right", padx=10, pady=10)

    def parse_stories(self):
        text = self.input_text.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some user stories first.")
            return

        self.status_label.configure(text="Parsing user stories...")
        self.root.update()

        try:
            self.current_stories = self.parser.parse_user_stories(text)
            if self.current_stories:
                self.status_label.configure(text=f"Parsed {len(self.current_stories)} user stories")
                messagebox.showinfo("Success", f"Successfully parsed {len(self.current_stories)} user stories!")
            else:
                self.status_label.configure(text="No valid user stories found")
                messagebox.showwarning("Warning", "No valid user stories could be parsed from the input.")
        except Exception as e:
            self.status_label.configure(text="Error parsing stories")
            messagebox.showerror("Error", f"Error parsing user stories: {str(e)}")

    def generate_prd(self):
        if not self.current_stories:
            messagebox.showwarning("Warning", "Please parse user stories first.")
            return

        self.status_label.configure(text="Generating PRD...")
        self.root.update()

        try:
            project_info = {
                'title': self.project_title.get() or "Untitled Project",
                'author': self.project_author.get() or "Unknown",
                'target_release': self.target_release.get() or "TBD",
                'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                'version': '1.0',
                'status': 'Draft'
            }

            self.current_prd = self.generator.generate_prd(self.current_stories, project_info)

            prd_text = ""
            for section in self.current_prd:
                prd_text += f"{'='*60}\n"
                prd_text += f"{section.title.upper()}\n"
                prd_text += f"{'='*60}\n\n"
                prd_text += f"{section.content}\n\n"

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", prd_text)

            self.status_label.configure(text="PRD generated successfully")

        except Exception as e:
            self.status_label.configure(text="Error generating PRD")
            messagebox.showerror("Error", f"Error generating PRD: {str(e)}")

    def export_pdf(self):
        if not self.current_prd:
            messagebox.showwarning("Warning", "Please generate a PRD first.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if filename:
            try:
                doc = SimpleDocTemplate(filename, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []

                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=18,
                    spaceAfter=30,
                )

                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=14,
                    spaceAfter=12,
                )

                for section in self.current_prd:
                    story.append(Paragraph(section.title, heading_style))
                    story.append(Spacer(1, 12))

                    content_lines = section.content.split('\n')
                    for line in content_lines:
                        if line.strip():
                            story.append(Paragraph(line, styles['Normal']))
                        else:
                            story.append(Spacer(1, 6))

                    story.append(Spacer(1, 20))

                doc.build(story)
                self.status_label.configure(text=f"PDF exported: {filename}")
                messagebox.showinfo("Success", f"PRD exported successfully to {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Error exporting PDF: {str(e)}")

    def export_text(self):
        if not self.current_prd:
            messagebox.showwarning("Warning", "Please generate a PRD first.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for section in self.current_prd:
                        f.write(f"{'='*60}\n")
                        f.write(f"{section.title.upper()}\n")
                        f.write(f"{'='*60}\n\n")
                        f.write(f"{section.content}\n\n")

                self.status_label.configure(text=f"Text exported: {filename}")
                messagebox.showinfo("Success", f"PRD exported successfully to {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Error exporting text file: {str(e)}")

    def load_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", content)
                self.status_label.configure(text=f"Loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {str(e)}")

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.current_stories = []
        self.current_prd = []
        self.status_label.configure(text="Ready")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PRDGeneratorApp()
    app.run()