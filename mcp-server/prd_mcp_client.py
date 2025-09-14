#!/usr/bin/env python3
"""
PRD Generator MCP Client Integration

Client-side integration that connects the PRD Generator GUI application
with the MCP server for enhanced AI capabilities.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
import subprocess
import sys
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prd-mcp-client")

class MCPClient:
    """Client for communicating with the PRD Generator MCP server"""

    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.process = None

    @asynccontextmanager
    async def connect(self):
        """Context manager for MCP server connection"""
        try:
            self.process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Initialize MCP session
            init_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "resources": {},
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "prd-generator-client",
                        "version": "1.0.0"
                    }
                }
            }

            await self._send_message(init_message)
            response = await self._receive_message()

            if response.get("error"):
                raise Exception(f"MCP initialization failed: {response['error']}")

            yield self

        finally:
            if self.process:
                self.process.terminate()
                await self.process.wait()

    async def _send_message(self, message: Dict[str, Any]):
        """Send JSON-RPC message to MCP server"""
        message_json = json.dumps(message) + '\n'
        self.process.stdin.write(message_json.encode())
        await self.process.stdin.drain()

    async def _receive_message(self) -> Dict[str, Any]:
        """Receive JSON-RPC message from MCP server"""
        line = await self.process.stdout.readline()
        return json.loads(line.decode().strip())

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get available MCP tools"""
        message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }

        await self._send_message(message)
        response = await self._receive_message()

        if response.get("error"):
            raise Exception(f"Failed to list tools: {response['error']}")

        return response.get("result", {}).get("tools", [])

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool"""
        message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }

        await self._send_message(message)
        response = await self._receive_message()

        if response.get("error"):
            raise Exception(f"Tool call failed: {response['error']}")

        return response.get("result")

class PRDEnhancer:
    """Integration layer for enhancing PRD Generator with AI capabilities"""

    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client

    async def fetch_jira_stories(self, config: Dict[str, str]) -> List[str]:
        """Fetch user stories from Jira"""
        try:
            result = await self.mcp_client.call_tool("fetch_jira_stories", {
                "project_key": config["project_key"],
                "base_url": config["base_url"],
                "email": config["email"],
                "api_token": config["api_token"],
                "jql": config.get("jql")
            })

            data = json.loads(result["content"][0]["text"])
            return data.get("stories", [])

        except Exception as e:
            logger.error(f"Failed to fetch Jira stories: {e}")
            return []

    async def analyze_user_stories(self, stories: List[str], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze user stories for quality and improvements"""
        analysis_results = []

        for story in stories:
            try:
                result = await self.mcp_client.call_tool("analyze_user_story", {
                    "story": story,
                    "context": context or {}
                })

                data = json.loads(result["content"][0]["text"])
                analysis_results.append({
                    "story": story,
                    "analysis": data
                })

            except Exception as e:
                logger.error(f"Failed to analyze story: {e}")
                analysis_results.append({
                    "story": story,
                    "analysis": {"error": str(e)}
                })

        return {
            "results": analysis_results,
            "summary": self._generate_analysis_summary(analysis_results)
        }

    async def get_improvement_suggestions(self, stories: List[str], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Get AI-powered improvement suggestions for user stories"""
        try:
            result = await self.mcp_client.call_tool("improve_user_stories", {
                "stories": stories,
                "context": context or {}
            })

            return json.loads(result["content"][0]["text"])

        except Exception as e:
            logger.error(f"Failed to get improvements: {e}")
            return {"error": str(e)}

    async def get_best_practices(self, domain: Optional[str] = None, focus_area: Optional[str] = None) -> Dict[str, Any]:
        """Get contextual best practices for user story writing"""
        try:
            params = {}
            if domain:
                params["domain"] = domain
            if focus_area:
                params["focus_area"] = focus_area

            result = await self.mcp_client.call_tool("get_best_practices", params)
            return json.loads(result["content"][0]["text"])

        except Exception as e:
            logger.error(f"Failed to get best practices: {e}")
            return {"error": str(e)}

    async def enhance_prd_content(self, prd_sections: Dict[str, Any], focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
        """Enhance PRD content with AI suggestions"""
        try:
            params = {"prd_sections": prd_sections}
            if focus_areas:
                params["enhancement_focus"] = focus_areas

            result = await self.mcp_client.call_tool("enhance_prd_content", params)
            return json.loads(result["content"][0]["text"])

        except Exception as e:
            logger.error(f"Failed to enhance PRD content: {e}")
            return {"error": str(e)}

    async def validate_prd_completeness(self, prd_content: str, standard: Optional[str] = None) -> Dict[str, Any]:
        """Validate PRD completeness against industry standards"""
        try:
            params = {"prd_content": prd_content}
            if standard:
                params["industry_standard"] = standard

            result = await self.mcp_client.call_tool("validate_prd_completeness", params)
            return json.loads(result["content"][0]["text"])

        except Exception as e:
            logger.error(f"Failed to validate PRD: {e}")
            return {"error": str(e)}

    def _generate_analysis_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of story analysis results"""
        total_stories = len(results)
        valid_analyses = [r for r in results if "error" not in r["analysis"]]

        if not valid_analyses:
            return {"error": "No valid analyses completed"}

        scores = [r["analysis"].get("analysis", {}).get("score", 0) for r in valid_analyses]
        avg_score = sum(scores) / len(scores) if scores else 0

        issues_count = sum(len(r["analysis"].get("analysis", {}).get("issues", [])) for r in valid_analyses)
        suggestions_count = sum(len(r["analysis"].get("improvements", [])) for r in valid_analyses)

        return {
            "total_stories": total_stories,
            "analyzed_stories": len(valid_analyses),
            "average_quality_score": round(avg_score, 1),
            "total_issues_found": issues_count,
            "total_suggestions": suggestions_count,
            "recommendation": "Focus on improvement" if avg_score < 60 else "Good quality stories"
        }

# Example usage functions
async def example_jira_integration():
    """Example of Jira integration"""
    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    async with client.connect():
        enhancer = PRDEnhancer(client)

        # Example Jira configuration
        jira_config = {
            "project_key": "PROJ",
            "base_url": "https://your-domain.atlassian.net",
            "email": "your-email@domain.com",
            "api_token": "your-api-token"
        }

        stories = await enhancer.fetch_jira_stories(jira_config)
        print(f"Fetched {len(stories)} stories from Jira")

        if stories:
            analysis = await enhancer.analyze_user_stories(stories[:3])  # Analyze first 3
            print(f"Analysis summary: {analysis['summary']}")

async def example_story_improvement():
    """Example of story improvement workflow"""
    server_command = [sys.executable, "server.py"]
    client = MCPClient(server_command)

    async with client.connect():
        enhancer = PRDEnhancer(client)

        sample_stories = [
            "User can login to the system",
            "As a manager, I want to see reports so that I can make decisions",
            "System should be fast and user-friendly"
        ]

        # Get analysis
        analysis = await enhancer.analyze_user_stories(sample_stories, {
            "project_type": "web_application",
            "domain": "enterprise"
        })

        print("Story Analysis Results:")
        for result in analysis["results"]:
            story = result["story"][:50] + "..."
            score = result["analysis"].get("analysis", {}).get("score", 0)
            print(f"  {story}: Score {score}/100")

        # Get improvements
        improvements = await enhancer.get_improvement_suggestions(sample_stories, {
            "project_type": "web_application",
            "domain": "enterprise"
        })

        print(f"\nImprovement suggestions available for {len(improvements.get('improvements', []))} stories")

if __name__ == "__main__":
    print("PRD Generator MCP Client - Example Usage")
    print("=" * 50)

    # Run examples
    asyncio.run(example_story_improvement())