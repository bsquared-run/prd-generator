#!/usr/bin/env python3
"""
Example: Jira Integration with PRD Generator

This example demonstrates how to connect to Jira, import user stories,
analyze them with AI, and generate an enhanced PRD.
"""

import asyncio
import sys
import os

# Add the MCP server to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp-server'))

from prd_mcp_client import MCPClient, PRDEnhancer

async def jira_to_prd_workflow():
    """Complete workflow: Jira → AI Analysis → Enhanced PRD"""

    print("🚀 Jira Integration Example")
    print("=" * 50)

    # Configuration (replace with your actual Jira details)
    jira_config = {
        "project_key": "PROJ",  # Your Jira project key
        "base_url": "https://your-company.atlassian.net",
        "email": "your-email@company.com",
        "api_token": "your-jira-api-token",
        "jql": 'project = "PROJ" AND issuetype = "Story" AND status = "To Do"'
    }

    server_command = [sys.executable, "../mcp-server/server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            enhancer = PRDEnhancer(client)

            print("📥 Step 1: Fetching stories from Jira...")
            # Note: This will fail without real Jira credentials
            # stories = await enhancer.fetch_jira_stories(jira_config)

            # For demo purposes, use sample stories
            sample_stories = [
                "As a project manager, I want to create user accounts so that team members can access the project management system. Priority: High Story Points: 5",
                "As a developer, I want to view project dashboards so that I can track progress and identify bottlenecks. Priority: High Story Points: 8",
                "As a team lead, I want to assign tasks to team members so that work can be distributed effectively. Priority: Medium Story Points: 3"
            ]

            print(f"✅ Using {len(sample_stories)} sample stories (replace with real Jira import)")

            print("\n🤖 Step 2: AI Analysis of stories...")
            analysis = await enhancer.analyze_user_stories(sample_stories, {
                "domain": "enterprise",
                "project_type": "web_application"
            })

            summary = analysis.get("summary", {})
            print(f"   • Average Quality Score: {summary.get('average_quality_score', 0)}/100")
            print(f"   • Issues Found: {summary.get('total_issues_found', 0)}")
            print(f"   • Recommendations: {summary.get('recommendation', 'N/A')}")

            print("\n🚀 Step 3: Getting improvement suggestions...")
            improvements = await enhancer.get_improvement_suggestions(sample_stories, {
                "domain": "enterprise",
                "project_type": "web_application"
            })

            print(f"✅ Generated improvements for {len(improvements.get('improvements', []))} stories")

            print("\n📚 Step 4: Loading best practices...")
            practices = await enhancer.get_best_practices(domain="enterprise")
            print("✅ Loaded enterprise-specific best practices")

            print("\n📋 Step 5: Enhanced PRD generation...")
            # This would integrate with your PRD generator
            prd_sections = {
                "executive_summary": "Sample executive summary for demonstration",
                "user_stories": sample_stories,
                "functional_requirements": [f"FR{i:03d}: {story[:50]}..." for i, story in enumerate(sample_stories, 1)]
            }

            enhanced_prd = await enhancer.enhance_prd_content(prd_sections, [
                "clarity", "completeness", "actionability"
            ])

            print("✅ PRD enhanced with AI recommendations")

            print("\n✅ Step 6: Validating PRD completeness...")
            sample_prd_content = """
            EXECUTIVE SUMMARY
            This PRD outlines the requirements for our project management system.

            USER STORIES
            As detailed above, we have 3 core user stories.

            FUNCTIONAL REQUIREMENTS
            The system shall provide user account management.
            """

            validation = await enhancer.validate_prd_completeness(sample_prd_content, "agile")

            score = validation.get("completeness_score", 0)
            missing = validation.get("missing_sections", [])

            print(f"   • Completeness Score: {score}%")
            print(f"   • Missing Sections: {len(missing)}")

            print("\n🎉 Complete workflow executed successfully!")
            print("Next steps: Integrate with your actual Jira instance and PRD generator.")

    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        print("Note: This example requires MCP server to be running and proper configuration.")

if __name__ == "__main__":
    print("Jira Integration Example for PRD Generator")
    print("Note: Update jira_config with your actual credentials")
    print()

    asyncio.run(jira_to_prd_workflow())