#!/usr/bin/env python3

def test_basic_parsing():
    print("Testing basic user story parsing...")

    test_input = """As a project manager, I want to create user accounts so that team members can access the project management system.
Priority: High
Story Points: 5

Acceptance Criteria:
- Users can register with email and password
- Email verification is required"""

    from prd_generator import UserStoryParser
    parser = UserStoryParser()

    try:
        stories = parser.parse_user_stories(test_input)
        print(f"SUCCESS: Parsed {len(stories)} stories")

        if stories:
            story = stories[0]
            print(f"  Title: {story.title}")
            print(f"  Priority: {story.priority}")
            print(f"  Story Points: {story.story_points}")
            print(f"  Acceptance Criteria: {len(story.acceptance_criteria)} items")

        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_parsing()
    print("Test completed:", "PASSED" if success else "FAILED")