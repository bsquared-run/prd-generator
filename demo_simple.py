#!/usr/bin/env python3

from prd_generator import UserStoryParser, PRDGenerator

def main():
    print("PRD Generator Demo Test")
    print("=" * 50)

    # Load sample user stories
    with open('sample_user_stories.txt', 'r', encoding='utf-8') as f:
        sample_stories = f.read()

    print("Sample User Stories Loaded:")
    print("-" * 30)
    print(sample_stories[:200] + "...\n")

    # Parse user stories
    parser = UserStoryParser()
    stories = parser.parse_user_stories(sample_stories)

    print(f"SUCCESS: Parsed {len(stories)} user stories!")
    print()

    # Show parsed stories
    for i, story in enumerate(stories, 1):
        print(f"Story {i}: {story.title}")
        print(f"  Priority: {story.priority}")
        if story.story_points:
            print(f"  Story Points: {story.story_points}")
        print(f"  Acceptance Criteria: {len(story.acceptance_criteria)} items")
        print()

    # Generate PRD
    generator = PRDGenerator()
    project_info = {
        'title': 'Demo Project Management System',
        'author': 'PRD Generator Demo',
        'target_release': '2024-Q1',
        'version': '1.0'
    }

    print("Generating PRD...")
    prd_sections = generator.generate_prd(stories, project_info)

    print(f"SUCCESS: Generated PRD with {len(prd_sections)} sections!")
    print()

    # Show PRD sections
    print("PRD Sections Generated:")
    print("-" * 30)
    for section in prd_sections:
        print(f"- {section.title}")

    print()
    print("Sample PRD Content (Executive Summary):")
    print("-" * 50)
    exec_summary = next(s for s in prd_sections if 'Executive' in s.title)
    print(exec_summary.content[:300] + "...")

    # Save a sample PRD to file
    with open('demo_output.txt', 'w', encoding='utf-8') as f:
        for section in prd_sections:
            f.write(f"{'='*60}\n")
            f.write(f"{section.title.upper()}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"{section.content}\n\n")

    print()
    print("Demo completed successfully!")
    print("Generated PRD saved to: demo_output.txt")
    print("GUI application should also be running!")

if __name__ == "__main__":
    main()