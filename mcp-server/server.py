#!/usr/bin/env python3
"""
PRD Generator MCP Server

An MCP (Model Context Protocol) server that provides AI-enhanced capabilities
for the PRD Generator application, including Jira/Confluence integration,
intelligent user story analysis, and contextual best practices guidance.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urlparse
import re
import requests
from datetime import datetime
import base64

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prd-generator-mcp")

class AtlassianIntegrator:
    """Handles Jira and Confluence API interactions"""

    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        self.auth = (email, api_token)

    def get_jira_issues(self, project_key: str, jql: Optional[str] = None) -> List[Dict]:
        """Fetch Jira issues for user story extraction"""
        if not jql:
            jql = f'project = "{project_key}" AND issuetype in ("Story", "Epic", "Task")'

        url = f"{self.base_url}/rest/api/3/search"
        params = {
            'jql': jql,
            'fields': 'summary,description,priority,labels,customfield_*,acceptance,story_points',
            'maxResults': 100
        }

        try:
            response = requests.get(url, auth=self.auth, params=params)
            response.raise_for_status()
            return response.json().get('issues', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Jira issues: {e}")
            return []

    def get_confluence_pages(self, space_key: str, query: Optional[str] = None) -> List[Dict]:
        """Fetch Confluence pages for requirements analysis"""
        url = f"{self.base_url}/wiki/rest/api/content"
        params = {
            'spaceKey': space_key,
            'type': 'page',
            'status': 'current',
            'expand': 'body.storage,version,space',
            'limit': 50
        }

        if query:
            params['title'] = query

        try:
            response = requests.get(url, auth=self.auth, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Confluence pages: {e}")
            return []

class UserStoryAnalyzer:
    """AI-powered user story analysis and improvement suggestions"""

    @staticmethod
    def analyze_story_quality(story: str) -> Dict[str, Any]:
        """Analyze user story quality and provide improvement suggestions"""
        analysis = {
            'score': 0,
            'issues': [],
            'suggestions': [],
            'format': 'unknown',
            'completeness': {}
        }

        # Check format
        gherkin_pattern = r'As a (.+?), I want (.+?) so that (.+?)(?:\.|$)'
        if re.search(gherkin_pattern, story, re.IGNORECASE):
            analysis['format'] = 'gherkin'
            analysis['score'] += 30
        elif 'given' in story.lower() or 'when' in story.lower() or 'then' in story.lower():
            analysis['format'] = 'bdd'
            analysis['score'] += 20
        else:
            analysis['format'] = 'free-form'
            analysis['issues'].append("Consider using Gherkin format (As a... I want... so that...)")

        # Check completeness
        has_acceptance_criteria = bool(re.search(r'acceptance criteria?:|ac:', story, re.IGNORECASE))
        has_priority = bool(re.search(r'priority:|prio:', story, re.IGNORECASE))
        has_story_points = bool(re.search(r'story points?:|points?:|sp:', story, re.IGNORECASE))

        analysis['completeness'] = {
            'acceptance_criteria': has_acceptance_criteria,
            'priority': has_priority,
            'story_points': has_story_points
        }

        if has_acceptance_criteria:
            analysis['score'] += 25
        else:
            analysis['issues'].append("Missing acceptance criteria")
            analysis['suggestions'].append("Add specific, testable acceptance criteria")

        if has_priority:
            analysis['score'] += 15
        else:
            analysis['suggestions'].append("Consider adding priority level (High/Medium/Low)")

        if has_story_points:
            analysis['score'] += 10
        else:
            analysis['suggestions'].append("Consider adding story points for estimation")

        # Check story clarity
        if len(story.split()) < 10:
            analysis['issues'].append("Story may be too brief")
            analysis['suggestions'].append("Add more context and details")

        # Check for ambiguous terms
        ambiguous_terms = ['easy', 'simple', 'quick', 'user-friendly', 'intuitive']
        found_ambiguous = [term for term in ambiguous_terms if term in story.lower()]
        if found_ambiguous:
            analysis['issues'].append(f"Ambiguous terms found: {', '.join(found_ambiguous)}")
            analysis['suggestions'].append("Replace ambiguous terms with specific, measurable criteria")

        return analysis

    @staticmethod
    def suggest_improvements(story: str, context: Optional[Dict] = None) -> List[str]:
        """Generate AI-powered improvement suggestions"""
        suggestions = []

        analysis = UserStoryAnalyzer.analyze_story_quality(story)

        # Format suggestions
        if analysis['format'] != 'gherkin':
            suggestions.append(
                "Convert to Gherkin format: 'As a [role], I want [functionality] so that [benefit]'"
            )

        # Context-aware suggestions
        if context and context.get('project_type'):
            project_type = context['project_type'].lower()
            if 'mobile' in project_type:
                suggestions.append("Consider mobile-specific aspects: touch interactions, offline functionality, performance")
            elif 'web' in project_type:
                suggestions.append("Consider web-specific aspects: browser compatibility, responsive design, accessibility")
            elif 'api' in project_type:
                suggestions.append("Consider API-specific aspects: rate limiting, authentication, error handling")

        return suggestions + analysis['suggestions']

class BestPracticesGuide:
    """Contextual best practices for user story writing"""

    @staticmethod
    def get_writing_guidelines() -> Dict[str, List[str]]:
        """Get comprehensive user story writing guidelines"""
        return {
            'structure': [
                "Use the Gherkin format: As a [role], I want [functionality] so that [benefit]",
                "Keep stories focused on a single piece of functionality",
                "Write from the user's perspective, not the system's",
                "Include the 'why' (benefit) to provide context and priority"
            ],
            'acceptance_criteria': [
                "Write testable, specific conditions",
                "Use Given-When-Then format for scenario-based criteria",
                "Include both positive and negative test cases",
                "Specify UI/UX requirements clearly",
                "Define data validation rules explicitly"
            ],
            'quality_checks': [
                "Ensure story is INVEST compliant (Independent, Negotiable, Valuable, Estimable, Small, Testable)",
                "Verify story can be completed in one sprint",
                "Check that success criteria are measurable",
                "Confirm story delivers business value"
            ],
            'prioritization': [
                "Use consistent priority levels (High/Medium/Low or P0/P1/P2/P3)",
                "Consider business impact and technical complexity",
                "Align with product roadmap and strategic goals",
                "Factor in dependencies and prerequisites"
            ]
        }

    @staticmethod
    def get_domain_specific_guidance(domain: str) -> List[str]:
        """Get domain-specific user story guidance"""
        guidance_map = {
            'fintech': [
                "Include compliance and regulatory requirements",
                "Specify security and data protection measures",
                "Define audit trail requirements",
                "Consider multi-currency and localization needs"
            ],
            'healthcare': [
                "Ensure HIPAA compliance considerations",
                "Include patient privacy and data security",
                "Specify clinical workflow integration",
                "Consider accessibility for diverse patient populations"
            ],
            'e-commerce': [
                "Include payment processing requirements",
                "Specify inventory management integration",
                "Define user account and profile management",
                "Consider multi-platform consistency"
            ],
            'saas': [
                "Include multi-tenant considerations",
                "Specify subscription and billing requirements",
                "Define user role and permission management",
                "Consider scalability and performance requirements"
            ]
        }

        return guidance_map.get(domain.lower(), [
            "Consider industry-specific compliance requirements",
            "Include relevant integration points",
            "Define appropriate user roles and permissions"
        ])

# Initialize the MCP server
app = Server("prd-generator-mcp")

# Global configuration
config = {
    'atlassian_integrator': None,
    'user_story_analyzer': UserStoryAnalyzer(),
    'best_practices_guide': BestPracticesGuide()
}

@app.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="best-practices://user-stories",
            name="User Story Best Practices",
            description="Comprehensive guidelines for writing effective user stories",
            mimeType="application/json"
        ),
        Resource(
            uri="templates://user-story-formats",
            name="User Story Templates",
            description="Templates and examples for different user story formats",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read resource content"""
    if uri == "best-practices://user-stories":
        return json.dumps(config['best_practices_guide'].get_writing_guidelines(), indent=2)
    elif uri == "templates://user-story-formats":
        templates = {
            "gherkin": {
                "format": "As a [role], I want [functionality] so that [benefit]",
                "example": "As a project manager, I want to create user accounts so that team members can access the project management system"
            },
            "bdd": {
                "format": "Given [context] When [action] Then [outcome]",
                "example": "Given I am on the login page When I enter valid credentials Then I should be logged into the system"
            },
            "job_story": {
                "format": "When I [situation], I want to [motivation], so I can [expected outcome]",
                "example": "When I'm reviewing project progress, I want to see visual dashboards, so I can quickly identify bottlenecks"
            }
        }
        return json.dumps(templates, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="fetch_jira_stories",
            description="Fetch user stories from Jira project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_key": {"type": "string", "description": "Jira project key"},
                    "jql": {"type": "string", "description": "Optional JQL query for filtering"},
                    "base_url": {"type": "string", "description": "Jira instance URL"},
                    "email": {"type": "string", "description": "User email"},
                    "api_token": {"type": "string", "description": "API token"}
                },
                "required": ["project_key", "base_url", "email", "api_token"]
            }
        ),
        Tool(
            name="fetch_confluence_requirements",
            description="Fetch requirements from Confluence pages",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_key": {"type": "string", "description": "Confluence space key"},
                    "query": {"type": "string", "description": "Optional page title query"},
                    "base_url": {"type": "string", "description": "Confluence instance URL"},
                    "email": {"type": "string", "description": "User email"},
                    "api_token": {"type": "string", "description": "API token"}
                },
                "required": ["space_key", "base_url", "email", "api_token"]
            }
        ),
        Tool(
            name="analyze_user_story",
            description="Analyze user story quality and provide improvement suggestions",
            inputSchema={
                "type": "object",
                "properties": {
                    "story": {"type": "string", "description": "User story text to analyze"},
                    "context": {
                        "type": "object",
                        "description": "Additional context for analysis",
                        "properties": {
                            "project_type": {"type": "string"},
                            "domain": {"type": "string"},
                            "team_size": {"type": "number"}
                        }
                    }
                },
                "required": ["story"]
            }
        ),
        Tool(
            name="improve_user_stories",
            description="Generate AI-powered improvements for user stories",
            inputSchema={
                "type": "object",
                "properties": {
                    "stories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of user story texts"
                    },
                    "context": {
                        "type": "object",
                        "description": "Project context for improvements",
                        "properties": {
                            "project_type": {"type": "string"},
                            "domain": {"type": "string"},
                            "target_audience": {"type": "string"}
                        }
                    }
                },
                "required": ["stories"]
            }
        ),
        Tool(
            name="get_best_practices",
            description="Get contextual best practices for user story writing",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Project domain (e.g., fintech, healthcare, e-commerce)"},
                    "focus_area": {"type": "string", "description": "Specific area to focus on (structure, acceptance_criteria, etc.)"}
                },
                "required": []
            }
        ),
        Tool(
            name="enhance_prd_content",
            description="Provide AI-powered enhancements for PRD content",
            inputSchema={
                "type": "object",
                "properties": {
                    "prd_sections": {
                        "type": "object",
                        "description": "PRD sections to enhance",
                        "properties": {
                            "executive_summary": {"type": "string"},
                            "user_stories": {"type": "array", "items": {"type": "string"}},
                            "functional_requirements": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "enhancement_focus": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Areas to focus enhancement on"
                    }
                },
                "required": ["prd_sections"]
            }
        ),
        Tool(
            name="validate_prd_completeness",
            description="Validate PRD completeness and suggest missing sections",
            inputSchema={
                "type": "object",
                "properties": {
                    "prd_content": {"type": "string", "description": "Complete PRD content to validate"},
                    "industry_standard": {"type": "string", "description": "Industry standard to validate against"}
                },
                "required": ["prd_content"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "fetch_jira_stories":
        integrator = AtlassianIntegrator(
            arguments["base_url"],
            arguments["email"],
            arguments["api_token"]
        )

        issues = integrator.get_jira_issues(
            arguments["project_key"],
            arguments.get("jql")
        )

        stories = []
        for issue in issues:
            fields = issue.get('fields', {})
            story_text = f"Title: {fields.get('summary', 'No title')}\n"

            if fields.get('description'):
                story_text += f"Description: {fields['description']}\n"

            if fields.get('priority'):
                story_text += f"Priority: {fields['priority']['name']}\n"

            # Extract custom fields that might contain story points
            for field_key, field_value in fields.items():
                if 'customfield' in field_key and field_value and 'story' in str(field_value).lower():
                    story_text += f"Story Points: {field_value}\n"

            stories.append(story_text)

        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "success",
                "stories_count": len(stories),
                "stories": stories
            }, indent=2)
        )]

    elif name == "fetch_confluence_requirements":
        integrator = AtlassianIntegrator(
            arguments["base_url"],
            arguments["email"],
            arguments["api_token"]
        )

        pages = integrator.get_confluence_pages(
            arguments["space_key"],
            arguments.get("query")
        )

        requirements = []
        for page in pages:
            content = page.get('body', {}).get('storage', {}).get('value', '')
            # Simple HTML tag removal for basic text extraction
            clean_content = re.sub(r'<[^>]+>', '', content)

            requirements.append({
                "title": page.get('title', 'No title'),
                "url": f"{arguments['base_url']}/wiki{page.get('_links', {}).get('webui', '')}",
                "content": clean_content[:1000] + "..." if len(clean_content) > 1000 else clean_content
            })

        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "success",
                "pages_count": len(requirements),
                "requirements": requirements
            }, indent=2)
        )]

    elif name == "analyze_user_story":
        analyzer = config['user_story_analyzer']
        story = arguments["story"]
        context = arguments.get("context")

        analysis = analyzer.analyze_story_quality(story)
        improvements = analyzer.suggest_improvements(story, context)

        result = {
            "analysis": analysis,
            "improvements": improvements,
            "recommendations": {
                "priority": "High" if analysis['score'] < 50 else "Medium" if analysis['score'] < 80 else "Low",
                "action_items": analysis['issues'][:3],  # Top 3 issues
                "next_steps": improvements[:3]  # Top 3 suggestions
            }
        }

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    elif name == "improve_user_stories":
        analyzer = config['user_story_analyzer']
        stories = arguments["stories"]
        context = arguments.get("context", {})

        improvements = []
        for i, story in enumerate(stories):
            analysis = analyzer.analyze_story_quality(story)
            suggestions = analyzer.suggest_improvements(story, context)

            improved_story = {
                "original": story,
                "score": analysis['score'],
                "improvements": suggestions,
                "enhanced_version": None  # Could be generated with AI model
            }

            # Generate enhanced version based on suggestions
            if analysis['format'] != 'gherkin' and 'as a' not in story.lower():
                # Attempt to convert to Gherkin format
                lines = story.split('\n')
                title = lines[0] if lines else story
                enhanced_story = f"As a user, I want {title.lower()} so that I can accomplish my goals"
                improved_story["enhanced_version"] = enhanced_story

            improvements.append(improved_story)

        return [TextContent(
            type="text",
            text=json.dumps({
                "improvements": improvements,
                "summary": f"Analyzed {len(stories)} stories, average score: {sum(imp['score'] for imp in improvements) / len(improvements):.1f}"
            }, indent=2)
        )]

    elif name == "get_best_practices":
        guide = config['best_practices_guide']
        domain = arguments.get("domain")
        focus_area = arguments.get("focus_area")

        guidelines = guide.get_writing_guidelines()
        result = {"general_guidelines": guidelines}

        if domain:
            result["domain_specific"] = guide.get_domain_specific_guidance(domain)

        if focus_area and focus_area in guidelines:
            result["focused_guidance"] = guidelines[focus_area]

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    elif name == "enhance_prd_content":
        prd_sections = arguments["prd_sections"]
        enhancement_focus = arguments.get("enhancement_focus", ["clarity", "completeness", "actionability"])

        enhancements = {}

        # Enhance executive summary
        if "executive_summary" in prd_sections:
            original = prd_sections["executive_summary"]
            enhancements["executive_summary"] = {
                "original": original,
                "suggestions": [
                    "Add quantifiable business metrics and success criteria",
                    "Include competitive analysis or market positioning",
                    "Specify target user segments more precisely",
                    "Add timeline and resource allocation overview"
                ]
            }

        # Enhance user stories
        if "user_stories" in prd_sections:
            stories = prd_sections["user_stories"]
            analyzer = config['user_story_analyzer']

            story_enhancements = []
            for story in stories:
                analysis = analyzer.analyze_story_quality(story)
                story_enhancements.append({
                    "story": story,
                    "quality_score": analysis['score'],
                    "improvements": analysis['suggestions'][:3]
                })

            enhancements["user_stories"] = story_enhancements

        return [TextContent(
            type="text",
            text=json.dumps(enhancements, indent=2)
        )]

    elif name == "validate_prd_completeness":
        prd_content = arguments["prd_content"]
        industry_standard = arguments.get("industry_standard", "general")

        # Define required sections for different standards
        required_sections = {
            "general": [
                "Executive Summary", "Product Overview", "User Stories",
                "Functional Requirements", "Acceptance Criteria",
                "Assumptions", "Success Metrics"
            ],
            "agile": [
                "Product Vision", "User Personas", "User Stories",
                "Acceptance Criteria", "Definition of Done",
                "Success Metrics", "Dependencies"
            ],
            "enterprise": [
                "Executive Summary", "Business Requirements", "Stakeholder Analysis",
                "Functional Requirements", "Non-Functional Requirements",
                "Risk Assessment", "Implementation Timeline", "Success Metrics"
            ]
        }

        sections_to_check = required_sections.get(industry_standard, required_sections["general"])

        missing_sections = []
        present_sections = []

        for section in sections_to_check:
            if section.lower() in prd_content.lower():
                present_sections.append(section)
            else:
                missing_sections.append(section)

        completeness_score = (len(present_sections) / len(sections_to_check)) * 100

        validation_result = {
            "completeness_score": completeness_score,
            "present_sections": present_sections,
            "missing_sections": missing_sections,
            "recommendations": [],
            "industry_standard": industry_standard
        }

        # Add specific recommendations
        if "Executive Summary" in missing_sections:
            validation_result["recommendations"].append("Add an Executive Summary with business context and objectives")

        if "Success Metrics" in missing_sections:
            validation_result["recommendations"].append("Include measurable success criteria and KPIs")

        if "Acceptance Criteria" in missing_sections:
            validation_result["recommendations"].append("Define clear acceptance criteria for all user stories")

        return [TextContent(
            type="text",
            text=json.dumps(validation_result, indent=2)
        )]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="prd-generator-mcp",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())