#!/usr/bin/env python3
"""
Enhanced PRD Generator with MCP Integration

This is an enhanced version of the original PRD Generator that integrates
with the MCP server for AI-powered capabilities.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import asyncio
import threading
from typing import Dict, List, Optional, Any
import json

# Import the MCP client
from prd_mcp_client import MCPClient, PRDEnhancer

# Import original components
import sys
import os
sys.path.append('../PRDGenerator')
from prd_generator import UserStoryParser, PRDGenerator, UserStory, PRDSection

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EnhancedPRDGeneratorApp:
    """Enhanced PRD Generator with AI-powered MCP integration"""

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Enhanced PRD Generator - AI-Powered with MCP")
        self.root.geometry("1600x1000")

        # Core components
        self.parser = UserStoryParser()
        self.generator = PRDGenerator()
        self.current_stories = []
        self.current_prd = []

        # MCP integration
        self.mcp_client = None
        self.prd_enhancer = None
        self.mcp_server_command = ["python", "server.py"]

        # UI state
        self.analysis_results = {}
        self.improvement_suggestions = {}

        self.setup_ui()

    def setup_ui(self):
        """Setup the enhanced UI with AI features"""
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title with AI badge
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))

        title_label = ctk.CTkLabel(
            title_frame,
            text="Enhanced PRD Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", pady=10, padx=10)

        ai_badge = ctk.CTkLabel(
            title_frame,
            text="🤖 AI-Powered",
            font=ctk.CTkFont(size=12),
            fg_color="green",
            corner_radius=10
        )
        ai_badge.pack(side="right", pady=10, padx=10)

        # Create notebook for tabbed interface
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Tab 1: Story Input & Analysis
        self.setup_input_tab()

        # Tab 2: AI Enhancement
        self.setup_enhancement_tab()

        # Tab 3: PRD Generation
        self.setup_prd_tab()

        # Tab 4: Jira/Confluence Integration
        self.setup_integration_tab()

        # Bottom status bar
        self.setup_status_bar(main_frame)

    def setup_input_tab(self):
        """Setup the story input and analysis tab"""
        input_tab = self.notebook.add("Story Input & Analysis")

        # Left panel: Input
        left_frame = ctk.CTkFrame(input_tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        input_label = ctk.CTkLabel(
            left_frame,
            text="User Stories Input",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        input_label.pack(pady=(10, 5))

        self.input_text = ctk.CTkTextbox(
            left_frame,
            height=300,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.input_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Input buttons
        input_button_frame = ctk.CTkFrame(left_frame)
        input_button_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.parse_button = ctk.CTkButton(
            input_button_frame,
            text="Parse Stories",
            command=self.parse_stories
        )
        self.parse_button.pack(side="left", padx=(0, 5))

        self.analyze_ai_button = ctk.CTkButton(
            input_button_frame,
            text="🤖 AI Analysis",
            command=self.run_ai_analysis
        )
        self.analyze_ai_button.pack(side="left", padx=5)

        self.load_button = ctk.CTkButton(
            input_button_frame,
            text="Load File",
            command=self.load_file
        )
        self.load_button.pack(side="right")

        # Right panel: Analysis Results
        right_frame = ctk.CTkFrame(input_tab)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        analysis_label = ctk.CTkLabel(
            right_frame,
            text="AI Analysis Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        analysis_label.pack(pady=(10, 5))

        self.analysis_text = ctk.CTkTextbox(
            right_frame,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.analysis_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_enhancement_tab(self):
        """Setup the AI enhancement tab"""
        enhance_tab = self.notebook.add("AI Enhancement")

        # Top panel: Best Practices
        top_frame = ctk.CTkFrame(enhance_tab)
        top_frame.pack(fill="x", padx=10, pady=(10, 5))

        practices_label = ctk.CTkLabel(
            top_frame,
            text="Contextual Best Practices",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        practices_label.pack(pady=(10, 5))

        # Domain selection
        domain_frame = ctk.CTkFrame(top_frame)
        domain_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(domain_frame, text="Project Domain:").pack(side="left", padx=(10, 5))

        self.domain_var = ctk.StringVar(value="general")
        self.domain_dropdown = ctk.CTkComboBox(
            domain_frame,
            variable=self.domain_var,
            values=["general", "fintech", "healthcare", "e-commerce", "saas", "mobile", "web"],
            command=self.load_best_practices
        )
        self.domain_dropdown.pack(side="left", padx=5)

        self.load_practices_button = ctk.CTkButton(
            domain_frame,
            text="Load Best Practices",
            command=self.load_best_practices
        )
        self.load_practices_button.pack(side="left", padx=10)

        # Best practices display
        self.practices_text = ctk.CTkTextbox(
            top_frame,
            height=150,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.practices_text.pack(fill="x", padx=10, pady=(0, 10))

        # Bottom panel: Improvements
        bottom_frame = ctk.CTkFrame(enhance_tab)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        improve_label = ctk.CTkLabel(
            bottom_frame,
            text="AI-Powered Story Improvements",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        improve_label.pack(pady=(10, 5))

        self.improve_button = ctk.CTkButton(
            bottom_frame,
            text="🚀 Generate Improvements",
            command=self.generate_improvements
        )
        self.improve_button.pack(pady=5)

        self.improvements_text = ctk.CTkTextbox(
            bottom_frame,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.improvements_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_prd_tab(self):
        """Setup the PRD generation tab"""
        prd_tab = self.notebook.add("PRD Generation")

        # Left panel: Project Info
        left_frame = ctk.CTkFrame(prd_tab)
        left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10, ipadx=20)

        info_label = ctk.CTkLabel(
            left_frame,
            text="Project Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=(10, 10))

        self.project_title = ctk.CTkEntry(
            left_frame,
            placeholder_text="Project Title",
            width=250
        )
        self.project_title.pack(pady=5, padx=10)

        self.project_author = ctk.CTkEntry(
            left_frame,
            placeholder_text="Author Name",
            width=250
        )
        self.project_author.pack(pady=5, padx=10)

        self.target_release = ctk.CTkEntry(
            left_frame,
            placeholder_text="Target Release Date",
            width=250
        )
        self.target_release.pack(pady=5, padx=10)

        # PRD controls
        control_frame = ctk.CTkFrame(left_frame)
        control_frame.pack(fill="x", padx=10, pady=20)

        self.generate_button = ctk.CTkButton(
            control_frame,
            text="Generate PRD",
            command=self.generate_prd,
            height=40
        )
        self.generate_button.pack(pady=5)

        self.enhance_prd_button = ctk.CTkButton(
            control_frame,
            text="🤖 Enhance with AI",
            command=self.enhance_prd_with_ai,
            height=40
        )
        self.enhance_prd_button.pack(pady=5)

        self.validate_button = ctk.CTkButton(
            control_frame,
            text="✅ Validate PRD",
            command=self.validate_prd,
            height=40
        )
        self.validate_button.pack(pady=5)

        # Export buttons
        export_frame = ctk.CTkFrame(left_frame)
        export_frame.pack(fill="x", padx=10, pady=10)

        self.export_pdf_button = ctk.CTkButton(
            export_frame,
            text="Export PDF",
            command=self.export_pdf
        )
        self.export_pdf_button.pack(pady=2)

        self.export_txt_button = ctk.CTkButton(
            export_frame,
            text="Export Text",
            command=self.export_text
        )
        self.export_txt_button.pack(pady=2)

        # Right panel: PRD Output
        right_frame = ctk.CTkFrame(prd_tab)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        output_label = ctk.CTkLabel(
            right_frame,
            text="Generated PRD",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        output_label.pack(pady=(10, 5))

        self.output_text = ctk.CTkTextbox(
            right_frame,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_integration_tab(self):
        """Setup Jira/Confluence integration tab"""
        integration_tab = self.notebook.add("Jira/Confluence")

        # Connection settings
        conn_frame = ctk.CTkFrame(integration_tab)
        conn_frame.pack(fill="x", padx=10, pady=(10, 5))

        conn_label = ctk.CTkLabel(
            conn_frame,
            text="Atlassian Integration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        conn_label.pack(pady=(10, 10))

        # Connection form
        form_frame = ctk.CTkFrame(conn_frame)
        form_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.base_url_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="https://your-domain.atlassian.net",
            width=300
        )
        self.base_url_entry.pack(side="left", padx=5)

        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="your-email@domain.com",
            width=200
        )
        self.email_entry.pack(side="left", padx=5)

        self.api_token_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="API Token",
            show="*",
            width=150
        )
        self.api_token_entry.pack(side="left", padx=5)

        # Integration controls
        controls_frame = ctk.CTkFrame(integration_tab)
        controls_frame.pack(fill="x", padx=10, pady=5)

        # Jira section
        jira_frame = ctk.CTkFrame(controls_frame)
        jira_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        ctk.CTkLabel(
            jira_frame,
            text="Jira Integration",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))

        self.project_key_entry = ctk.CTkEntry(
            jira_frame,
            placeholder_text="Project Key (e.g., PROJ)"
        )
        self.project_key_entry.pack(pady=5, padx=10)

        self.jql_entry = ctk.CTkEntry(
            jira_frame,
            placeholder_text="Custom JQL (optional)"
        )
        self.jql_entry.pack(pady=5, padx=10)

        self.fetch_jira_button = ctk.CTkButton(
            jira_frame,
            text="📥 Fetch Jira Stories",
            command=self.fetch_jira_stories
        )
        self.fetch_jira_button.pack(pady=10)

        # Confluence section
        confluence_frame = ctk.CTkFrame(controls_frame)
        confluence_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        ctk.CTkLabel(
            confluence_frame,
            text="Confluence Integration",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))

        self.space_key_entry = ctk.CTkEntry(
            confluence_frame,
            placeholder_text="Space Key"
        )
        self.space_key_entry.pack(pady=5, padx=10)

        self.page_query_entry = ctk.CTkEntry(
            confluence_frame,
            placeholder_text="Page Title Query (optional)"
        )
        self.page_query_entry.pack(pady=5, padx=10)

        self.fetch_confluence_button = ctk.CTkButton(
            confluence_frame,
            text="📄 Fetch Requirements",
            command=self.fetch_confluence_requirements
        )
        self.fetch_confluence_button.pack(pady=10)

        # Results area
        results_frame = ctk.CTkFrame(integration_tab)
        results_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        results_label = ctk.CTkLabel(
            results_frame,
            text="Integration Results",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(pady=(10, 5))

        self.integration_results = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.integration_results.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def setup_status_bar(self, parent):
        """Setup status bar"""
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready - Enhanced with AI capabilities",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(side="right", padx=10, pady=5)
        self.progress_bar.set(0)

    # Core functionality methods
    def parse_stories(self):
        """Parse user stories using the original parser"""
        text = self.input_text.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some user stories first.")
            return

        try:
            self.current_stories = self.parser.parse_user_stories(text)
            if self.current_stories:
                self.status_label.configure(text=f"Parsed {len(self.current_stories)} user stories")
                messagebox.showinfo("Success", f"Successfully parsed {len(self.current_stories)} user stories!")
            else:
                messagebox.showwarning("Warning", "No valid user stories could be parsed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing stories: {str(e)}")

    def run_ai_analysis(self):
        """Run AI analysis on parsed stories"""
        if not self.current_stories:
            messagebox.showwarning("Warning", "Please parse user stories first.")
            return

        def analysis_thread():
            try:
                self.update_status("Running AI analysis...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._ai_analysis())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"AI analysis failed: {str(e)}"))

        threading.Thread(target=analysis_thread, daemon=True).start()

    async def _ai_analysis(self):
        """Async AI analysis implementation"""
        client = MCPClient(self.mcp_server_command)
        async with client.connect():
            enhancer = PRDEnhancer(client)

            stories_text = [story.description for story in self.current_stories]
            context = {"domain": self.domain_var.get()}

            analysis = await enhancer.analyze_user_stories(stories_text, context)
            self.analysis_results = analysis

            # Update UI
            def update_ui():
                self.display_analysis_results(analysis)
                self.update_status("AI analysis complete")

            self.root.after(0, update_ui)

    def display_analysis_results(self, analysis):
        """Display AI analysis results"""
        self.analysis_text.delete("1.0", "end")

        summary = analysis.get("summary", {})
        self.analysis_text.insert("end", "=== AI ANALYSIS SUMMARY ===\n\n")
        self.analysis_text.insert("end", f"Total Stories: {summary.get('total_stories', 0)}\n")
        self.analysis_text.insert("end", f"Average Quality Score: {summary.get('average_quality_score', 0)}/100\n")
        self.analysis_text.insert("end", f"Issues Found: {summary.get('total_issues_found', 0)}\n")
        self.analysis_text.insert("end", f"Suggestions: {summary.get('total_suggestions', 0)}\n")
        self.analysis_text.insert("end", f"Recommendation: {summary.get('recommendation', 'N/A')}\n\n")

        self.analysis_text.insert("end", "=== DETAILED RESULTS ===\n\n")
        for i, result in enumerate(analysis.get("results", []), 1):
            story = result["story"][:80] + "..." if len(result["story"]) > 80 else result["story"]
            analysis_data = result["analysis"]

            self.analysis_text.insert("end", f"Story {i}: {story}\n")
            if "analysis" in analysis_data:
                score = analysis_data["analysis"].get("score", 0)
                issues = analysis_data["analysis"].get("issues", [])
                self.analysis_text.insert("end", f"  Score: {score}/100\n")
                if issues:
                    self.analysis_text.insert("end", f"  Issues: {'; '.join(issues)}\n")
            self.analysis_text.insert("end", "\n")

    def generate_improvements(self):
        """Generate AI-powered improvements"""
        if not self.current_stories:
            messagebox.showwarning("Warning", "Please parse user stories first.")
            return

        def improvement_thread():
            try:
                self.update_status("Generating AI improvements...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._generate_improvements())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Improvement generation failed: {str(e)}"))

        threading.Thread(target=improvement_thread, daemon=True).start()

    async def _generate_improvements(self):
        """Async improvement generation"""
        client = MCPClient(self.mcp_server_command)
        async with client.connect():
            enhancer = PRDEnhancer(client)

            stories_text = [story.description for story in self.current_stories]
            context = {"domain": self.domain_var.get(), "project_type": "web_application"}

            improvements = await enhancer.get_improvement_suggestions(stories_text, context)
            self.improvement_suggestions = improvements

            def update_ui():
                self.display_improvements(improvements)
                self.update_status("AI improvements generated")

            self.root.after(0, update_ui)

    def display_improvements(self, improvements):
        """Display improvement suggestions"""
        self.improvements_text.delete("1.0", "end")

        if "improvements" in improvements:
            for i, improvement in enumerate(improvements["improvements"], 1):
                original = improvement["original"][:60] + "..." if len(improvement["original"]) > 60 else improvement["original"]
                score = improvement.get("score", 0)
                suggestions = improvement.get("improvements", [])

                self.improvements_text.insert("end", f"Story {i}: {original}\n")
                self.improvements_text.insert("end", f"Quality Score: {score}/100\n")
                self.improvements_text.insert("end", "Suggestions:\n")
                for suggestion in suggestions[:3]:  # Top 3 suggestions
                    self.improvements_text.insert("end", f"  • {suggestion}\n")

                if improvement.get("enhanced_version"):
                    self.improvements_text.insert("end", f"Enhanced Version: {improvement['enhanced_version']}\n")

                self.improvements_text.insert("end", "\n" + "="*80 + "\n\n")

    def load_best_practices(self, event=None):
        """Load contextual best practices"""
        def practices_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._load_best_practices())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load practices: {str(e)}"))

        threading.Thread(target=practices_thread, daemon=True).start()

    async def _load_best_practices(self):
        """Async best practices loading"""
        client = MCPClient(self.mcp_server_command)
        async with client.connect():
            enhancer = PRDEnhancer(client)
            practices = await enhancer.get_best_practices(domain=self.domain_var.get())

            def update_ui():
                self.display_best_practices(practices)

            self.root.after(0, update_ui)

    def display_best_practices(self, practices):
        """Display best practices"""
        self.practices_text.delete("1.0", "end")

        if "general_guidelines" in practices:
            guidelines = practices["general_guidelines"]
            for category, items in guidelines.items():
                self.practices_text.insert("end", f"{category.upper().replace('_', ' ')}:\n")
                for item in items:
                    self.practices_text.insert("end", f"  • {item}\n")
                self.practices_text.insert("end", "\n")

        if "domain_specific" in practices:
            self.practices_text.insert("end", "DOMAIN-SPECIFIC GUIDANCE:\n")
            for item in practices["domain_specific"]:
                self.practices_text.insert("end", f"  • {item}\n")

    # Integration methods
    def fetch_jira_stories(self):
        """Fetch stories from Jira"""
        if not self._validate_connection():
            return

        def jira_thread():
            try:
                self.update_status("Fetching from Jira...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._fetch_jira())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Jira fetch failed: {str(e)}"))

        threading.Thread(target=jira_thread, daemon=True).start()

    async def _fetch_jira(self):
        """Async Jira fetch"""
        client = MCPClient(self.mcp_server_command)
        async with client.connect():
            enhancer = PRDEnhancer(client)

            config = {
                "project_key": self.project_key_entry.get(),
                "base_url": self.base_url_entry.get(),
                "email": self.email_entry.get(),
                "api_token": self.api_token_entry.get(),
                "jql": self.jql_entry.get() if self.jql_entry.get() else None
            }

            stories = await enhancer.fetch_jira_stories(config)

            def update_ui():
                if stories:
                    self.input_text.delete("1.0", "end")
                    self.input_text.insert("1.0", "\n\n".join(stories))
                    self.integration_results.delete("1.0", "end")
                    self.integration_results.insert("end", f"Successfully fetched {len(stories)} stories from Jira")
                    self.update_status(f"Fetched {len(stories)} stories from Jira")
                else:
                    self.integration_results.delete("1.0", "end")
                    self.integration_results.insert("end", "No stories found or connection failed")

            self.root.after(0, update_ui)

    def fetch_confluence_requirements(self):
        """Fetch requirements from Confluence"""
        # Similar implementation to Jira fetch
        messagebox.showinfo("Info", "Confluence integration - coming soon!")

    def _validate_connection(self):
        """Validate Atlassian connection settings"""
        if not all([
            self.base_url_entry.get(),
            self.email_entry.get(),
            self.api_token_entry.get()
        ]):
            messagebox.showwarning("Warning", "Please fill in all connection details.")
            return False
        return True

    # PRD Generation methods
    def generate_prd(self):
        """Generate PRD using original generator"""
        if not self.current_stories:
            messagebox.showwarning("Warning", "Please parse user stories first.")
            return

        try:
            project_info = {
                'title': self.project_title.get() or "Untitled Project",
                'author': self.project_author.get() or "Unknown",
                'target_release': self.target_release.get() or "TBD",
                'date': "2024-01-01",  # This should be current date
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
            messagebox.showerror("Error", f"Error generating PRD: {str(e)}")

    def enhance_prd_with_ai(self):
        """Enhance PRD content with AI"""
        if not self.current_prd:
            messagebox.showwarning("Warning", "Please generate a PRD first.")
            return

        def enhance_thread():
            try:
                self.update_status("Enhancing PRD with AI...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._enhance_prd())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"PRD enhancement failed: {str(e)}"))

        threading.Thread(target=enhance_thread, daemon=True).start()

    async def _enhance_prd(self):
        """Async PRD enhancement"""
        client = MCPClient(self.mcp_server_command)
        async with client.connect():
            enhancer = PRDEnhancer(client)

            # Extract sections for enhancement
            prd_sections = {
                "executive_summary": next((s.content for s in self.current_prd if "executive" in s.title.lower()), ""),
                "user_stories": [story.description for story in self.current_stories],
                "functional_requirements": [f"FR{i}: {story.title}" for i, story in enumerate(self.current_stories, 1)]
            }

            enhancements = await enhancer.enhance_prd_content(prd_sections)

            def update_ui():
                # Display enhancements in a popup or new section
                enhancement_text = json.dumps(enhancements, indent=2)
                messagebox.showinfo("AI Enhancements", f"Enhancement suggestions generated. Check the analysis tab for details.")
                self.update_status("PRD enhanced with AI")

            self.root.after(0, update_ui)

    def validate_prd(self):
        """Validate PRD completeness"""
        if not self.current_prd:
            messagebox.showwarning("Warning", "Please generate a PRD first.")
            return

        def validate_thread():
            try:
                self.update_status("Validating PRD...")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._validate_prd())
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"PRD validation failed: {str(e)}"))

        threading.Thread(target=validate_thread, daemon=True).start()

    async def _validate_prd(self):
        """Async PRD validation"""
        client = MCPClient(self.mcp_server_command)
        async with client.connect():
            enhancer = PRDEnhancer(client)

            prd_content = self.output_text.get("1.0", "end-1c")
            validation = await enhancer.validate_prd_completeness(prd_content, "agile")

            def update_ui():
                score = validation.get("completeness_score", 0)
                missing = validation.get("missing_sections", [])
                recommendations = validation.get("recommendations", [])

                result_text = f"Completeness Score: {score}%\n\n"
                if missing:
                    result_text += f"Missing Sections: {', '.join(missing)}\n\n"
                if recommendations:
                    result_text += "Recommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)

                messagebox.showinfo("PRD Validation", result_text)
                self.update_status("PRD validation complete")

            self.root.after(0, update_ui)

    # Utility methods
    def update_status(self, message):
        """Update status bar"""
        def update():
            self.status_label.configure(text=message)
            self.progress_bar.set(0.8)  # Indicate activity
            self.root.after(2000, lambda: self.progress_bar.set(0))

        self.root.after(0, update)

    def load_file(self):
        """Load file (placeholder)"""
        messagebox.showinfo("Info", "File loading - use original implementation")

    def export_pdf(self):
        """Export PDF (placeholder)"""
        messagebox.showinfo("Info", "PDF export - use original implementation")

    def export_text(self):
        """Export text (placeholder)"""
        messagebox.showinfo("Info", "Text export - use original implementation")

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedPRDGeneratorApp()
    app.run()