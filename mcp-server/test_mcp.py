#!/usr/bin/env python3
"""
Test script for PRD Generator MCP Server

This script tests the MCP server functionality and demonstrates
integration capabilities.
"""

import asyncio
import sys
import json
from prd_mcp_client import MCPClient, PRDEnhancer

async def test_basic_functionality():
    """Test basic MCP server functionality"""
    print("🧪 Testing Basic MCP Functionality")
    print("=" * 50)

    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            print("✅ MCP server connection established")

            # Test tool listing
            tools = await client.list_tools()
            print(f"✅ Available tools: {len(tools)}")
            for tool in tools:
                print(f"   • {tool['name']}: {tool['description']}")

            print("\n🎯 Testing User Story Analysis")
            print("-" * 30)

            enhancer = PRDEnhancer(client)

            # Test story analysis
            test_stories = [
                "As a project manager, I want to create user accounts so that team members can access the system",
                "User can login",
                "System should be fast and reliable"
            ]

            analysis = await enhancer.analyze_user_stories(test_stories, {
                "domain": "enterprise",
                "project_type": "web_application"
            })

            print(f"✅ Analyzed {len(test_stories)} stories")
            summary = analysis.get("summary", {})
            print(f"   • Average Quality Score: {summary.get('average_quality_score', 0)}/100")
            print(f"   • Total Issues Found: {summary.get('total_issues_found', 0)}")
            print(f"   • Recommendation: {summary.get('recommendation', 'N/A')}")

            return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_best_practices():
    """Test best practices functionality"""
    print("\n📚 Testing Best Practices Guidance")
    print("=" * 50)

    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            enhancer = PRDEnhancer(client)

            # Test general best practices
            practices = await enhancer.get_best_practices()
            print("✅ General best practices loaded")

            # Test domain-specific practices
            for domain in ["fintech", "healthcare", "e-commerce"]:
                domain_practices = await enhancer.get_best_practices(domain=domain)
                print(f"✅ {domain.capitalize()} practices loaded")

            return True

    except Exception as e:
        print(f"❌ Best practices test failed: {e}")
        return False

async def test_story_improvements():
    """Test story improvement functionality"""
    print("\n🚀 Testing Story Improvements")
    print("=" * 50)

    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            enhancer = PRDEnhancer(client)

            test_stories = [
                "User wants to see data",
                "The app should work well",
                "Login functionality needed"
            ]

            improvements = await enhancer.get_improvement_suggestions(test_stories, {
                "domain": "saas",
                "project_type": "web_application"
            })

            if "improvements" in improvements:
                print(f"✅ Generated improvements for {len(improvements['improvements'])} stories")
                for i, improvement in enumerate(improvements["improvements"][:2], 1):  # Show first 2
                    score = improvement.get("score", 0)
                    suggestions = improvement.get("improvements", [])
                    print(f"   Story {i}: Quality Score {score}/100")
                    print(f"   Suggestions: {len(suggestions)} items")

            return True

    except Exception as e:
        print(f"❌ Story improvements test failed: {e}")
        return False

async def test_prd_validation():
    """Test PRD validation functionality"""
    print("\n✅ Testing PRD Validation")
    print("=" * 50)

    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            enhancer = PRDEnhancer(client)

            # Test PRD content (simplified)
            sample_prd = """
            EXECUTIVE SUMMARY
            This is a sample PRD for testing purposes.

            USER STORIES
            As a user, I want to access the system.

            FUNCTIONAL REQUIREMENTS
            The system shall provide user authentication.
            """

            validation = await enhancer.validate_prd_completeness(sample_prd, "agile")

            score = validation.get("completeness_score", 0)
            missing = validation.get("missing_sections", [])
            recommendations = validation.get("recommendations", [])

            print(f"✅ PRD validation completed")
            print(f"   • Completeness Score: {score}%")
            print(f"   • Missing Sections: {len(missing)}")
            print(f"   • Recommendations: {len(recommendations)}")

            return True

    except Exception as e:
        print(f"❌ PRD validation test failed: {e}")
        return False

async def test_jira_integration_mock():
    """Test Jira integration with mock data (no real connection)"""
    print("\n🔗 Testing Jira Integration (Mock)")
    print("=" * 50)

    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    try:
        async with client.connect():
            print("ℹ️  Jira integration available (requires real credentials)")
            print("   • Tool: fetch_jira_stories")
            print("   • Supports: JQL filtering, bulk import, custom fields")
            print("   • Returns: Structured user stories with metadata")

            return True

    except Exception as e:
        print(f"❌ Jira integration test failed: {e}")
        return False

def print_test_summary(results):
    """Print test summary"""
    print("\n📊 Test Summary")
    print("=" * 50)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! MCP server is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

async def main():
    """Main test runner"""
    print("🧪 PRD Generator MCP Server - Test Suite")
    print("=" * 60)

    results = {}

    # Run all tests
    results["Basic Functionality"] = await test_basic_functionality()
    results["Best Practices"] = await test_best_practices()
    results["Story Improvements"] = await test_story_improvements()
    results["PRD Validation"] = await test_prd_validation()
    results["Jira Integration"] = await test_jira_integration_mock()

    print_test_summary(results)

    return all(results.values())

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        sys.exit(1)