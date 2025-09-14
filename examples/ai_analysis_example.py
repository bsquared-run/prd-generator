#!/usr/bin/env python3
"""
Example: AI-Powered User Story Analysis

This example demonstrates the AI analysis capabilities
of the PRD Generator MCP server.
"""

import asyncio
import sys
import os

# Add the MCP server to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp-server'))

from prd_mcp_client import MCPClient, PRDEnhancer

async def ai_analysis_demo():
    """Demonstrate AI analysis capabilities"""

    print("🤖 AI Analysis Example")
    print("=" * 50)

    # Sample stories with varying quality levels
    test_stories = [
        # High quality Gherkin story
        """As a project manager, I want to create user accounts so that team members can access the project management system.
        Priority: High
        Story Points: 5

        Acceptance Criteria:
        - Users can register with email and password
        - Email verification is required before account activation
        - Password must meet security requirements (8+ chars, special chars)
        - Users receive welcome email with getting started guide
        - Account creation is logged for audit purposes""",

        # Medium quality story
        """As a developer, I want to view project dashboards.
        Priority: Medium

        Acceptance Criteria:
        - Dashboard shows project progress
        - Can see task assignments""",

        # Low quality story
        """User needs login functionality.
        Should be easy and fast.""",

        # Free-form story
        """The system should allow managers to generate reports for stakeholder meetings.
        This is important for executive communication."""
    ]

    server_command = [sys.executable, "../mcp-server/server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            enhancer = PRDEnhancer(client)

            print("📊 Analyzing story quality...")
            analysis = await enhancer.analyze_user_stories(test_stories, {
                "domain": "enterprise",
                "project_type": "web_application",
                "team_size": 8
            })

            # Display overall summary
            summary = analysis.get("summary", {})
            print(f"\n📈 Overall Analysis Summary:")
            print(f"   • Total Stories: {summary.get('total_stories', 0)}")
            print(f"   • Average Quality Score: {summary.get('average_quality_score', 0):.1f}/100")
            print(f"   • Total Issues Found: {summary.get('total_issues_found', 0)}")
            print(f"   • Total Suggestions: {summary.get('total_suggestions', 0)}")
            print(f"   • Recommendation: {summary.get('recommendation', 'N/A')}")

            # Display detailed analysis for each story
            print(f"\n📋 Detailed Story Analysis:")
            print("-" * 60)

            for i, result in enumerate(analysis.get("results", []), 1):
                story_preview = result["story"][:80] + "..." if len(result["story"]) > 80 else result["story"]
                analysis_data = result.get("analysis", {})

                print(f"\nStory {i}: {story_preview}")

                if "analysis" in analysis_data:
                    story_analysis = analysis_data["analysis"]
                    score = story_analysis.get("score", 0)
                    format_type = story_analysis.get("format", "unknown")
                    issues = story_analysis.get("issues", [])
                    completeness = story_analysis.get("completeness", {})

                    print(f"   Quality Score: {score}/100")
                    print(f"   Format: {format_type}")
                    print(f"   Completeness:")
                    for aspect, present in completeness.items():
                        status = "✅" if present else "❌"
                        print(f"     {status} {aspect.replace('_', ' ').title()}")

                    if issues:
                        print(f"   Issues Found:")
                        for issue in issues:
                            print(f"     • {issue}")

                if "improvements" in analysis_data:
                    improvements = analysis_data["improvements"]
                    if improvements:
                        print(f"   Top Suggestions:")
                        for suggestion in improvements[:2]:  # Show top 2
                            print(f"     → {suggestion}")

            print("\n🚀 Generating Improvement Recommendations...")
            improvements = await enhancer.get_improvement_suggestions(test_stories, {
                "domain": "enterprise",
                "project_type": "web_application",
                "target_audience": "development_team"
            })

            if "improvements" in improvements:
                print(f"\n✨ AI-Generated Improvements:")
                print("-" * 60)

                for i, improvement in enumerate(improvements["improvements"], 1):
                    original_preview = improvement["original"][:60] + "..." if len(improvement["original"]) > 60 else improvement["original"]
                    score = improvement.get("score", 0)
                    suggestions = improvement.get("improvements", [])

                    print(f"\nStory {i}: {original_preview}")
                    print(f"   Current Score: {score}/100")

                    if improvement.get("enhanced_version"):
                        print(f"   Enhanced Version:")
                        print(f"     {improvement['enhanced_version']}")

                    if suggestions:
                        print(f"   Improvement Areas:")
                        for suggestion in suggestions[:3]:  # Top 3 suggestions
                            print(f"     • {suggestion}")

            print("\n📚 Loading Best Practices...")
            practices = await enhancer.get_best_practices(domain="enterprise")

            if "general_guidelines" in practices:
                print(f"\n💡 Best Practices for Enterprise Domain:")
                guidelines = practices["general_guidelines"]

                # Show structure guidelines
                if "structure" in guidelines:
                    print(f"\n   Story Structure:")
                    for guideline in guidelines["structure"][:2]:  # Top 2
                        print(f"     • {guideline}")

                # Show acceptance criteria guidelines
                if "acceptance_criteria" in guidelines:
                    print(f"\n   Acceptance Criteria:")
                    for guideline in guidelines["acceptance_criteria"][:2]:  # Top 2
                        print(f"     • {guideline}")

            print("\n🎉 AI Analysis Complete!")
            print("\nKey Insights:")
            print("• Higher quality stories have better structure and clear acceptance criteria")
            print("• Gherkin format (As a... I want... so that...) scores highest")
            print("• Specific, measurable acceptance criteria improve testability")
            print("• Domain context helps provide relevant improvement suggestions")

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("Note: Ensure MCP server is available and dependencies are installed.")

if __name__ == "__main__":
    print("AI Analysis Example for PRD Generator")
    print("This demonstrates the quality assessment and improvement capabilities.")
    print()

    asyncio.run(ai_analysis_demo())