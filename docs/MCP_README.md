# PRD Generator MCP Server

An advanced Model Context Protocol (MCP) server that enhances the PRD Generator with AI-powered capabilities, including Jira/Confluence integration, intelligent user story analysis, and contextual best practices guidance.

## 🚀 Features

### 🤖 AI-Powered Analysis
- **User Story Quality Assessment**: Automatic scoring and improvement suggestions
- **Contextual Best Practices**: Domain-specific guidance for different industries
- **PRD Enhancement**: AI-powered content improvement and validation
- **Completeness Validation**: Industry-standard PRD structure validation

### 🔗 Atlassian Integration
- **Jira Integration**: Direct import of user stories from Jira projects
- **Confluence Integration**: Requirements extraction from Confluence pages
- **JQL Support**: Advanced filtering for story selection
- **Bulk Import**: Efficient processing of multiple stories

### 📊 Smart Analytics
- **Quality Scoring**: Numerical assessment of user story quality
- **Issue Detection**: Automatic identification of common problems
- **Improvement Suggestions**: AI-generated enhancement recommendations
- **Progress Tracking**: Story refinement progress monitoring

## 🏗️ Architecture

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Enhanced GUI      │    │   MCP Client         │    │   MCP Server        │
│   Application       │◄──►│   Integration        │◄──►│   AI Engine         │
│                     │    │                      │    │                     │
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
                                                               │
                                                               ▼
                                                      ┌─────────────────────┐
                                                      │   Atlassian APIs    │
                                                      │   • Jira REST API   │
                                                      │   • Confluence API  │
                                                      └─────────────────────┘
```

## 📋 Available MCP Tools

### 1. `fetch_jira_stories`
Fetch user stories from Jira projects with customizable filtering.

**Parameters:**
- `project_key`: Jira project key (e.g., "PROJ")
- `base_url`: Jira instance URL
- `email`: User email address
- `api_token`: Jira API token
- `jql`: Optional JQL query for filtering

**Example:**
```json
{
  "project_key": "PROJ",
  "base_url": "https://company.atlassian.net",
  "email": "user@company.com",
  "api_token": "your-token",
  "jql": "issuetype = Story AND status = 'To Do'"
}
```

### 2. `analyze_user_story`
Analyze individual user stories for quality and completeness.

**Parameters:**
- `story`: User story text to analyze
- `context`: Optional project context (domain, type, etc.)

**Returns:**
- Quality score (0-100)
- Identified issues
- Improvement suggestions
- Format assessment

### 3. `improve_user_stories`
Generate AI-powered improvements for multiple user stories.

**Parameters:**
- `stories`: Array of user story texts
- `context`: Project context for tailored suggestions

**Returns:**
- Enhanced versions of stories
- Quality improvements
- Suggested modifications

### 4. `get_best_practices`
Retrieve contextual best practices for user story writing.

**Parameters:**
- `domain`: Project domain (fintech, healthcare, e-commerce, etc.)
- `focus_area`: Specific focus area (optional)

**Returns:**
- General guidelines
- Domain-specific recommendations
- Focused guidance

### 5. `enhance_prd_content`
Provide AI-powered enhancements for PRD sections.

**Parameters:**
- `prd_sections`: PRD content sections to enhance
- `enhancement_focus`: Areas to focus on

**Returns:**
- Section-specific improvements
- Content enhancement suggestions
- Quality recommendations

### 6. `validate_prd_completeness`
Validate PRD against industry standards.

**Parameters:**
- `prd_content`: Complete PRD text
- `industry_standard`: Standard to validate against

**Returns:**
- Completeness score
- Missing sections
- Recommendations

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Atlassian Integration
Set up your Atlassian credentials:
- Generate API tokens from Atlassian Account Settings
- Note your instance URL (e.g., `https://company.atlassian.net`)
- Ensure appropriate project/space permissions

### 3. Run MCP Server
```bash
python server.py
```

### 4. Use Enhanced GUI Application
```bash
python enhanced_prd_generator.py
```

## 🎯 Usage Examples

### Basic Story Analysis
```python
from prd_mcp_client import MCPClient, PRDEnhancer
import asyncio

async def analyze_stories():
    client = MCPClient(["python", "server.py"])
    async with client.connect():
        enhancer = PRDEnhancer(client)

        stories = [
            "As a user, I want to login",
            "The system should be fast and reliable"
        ]

        analysis = await enhancer.analyze_user_stories(stories)
        print(f"Average quality score: {analysis['summary']['average_quality_score']}")

asyncio.run(analyze_stories())
```

### Jira Integration
```python
async def fetch_from_jira():
    client = MCPClient(["python", "server.py"])
    async with client.connect():
        enhancer = PRDEnhancer(client)

        config = {
            "project_key": "MYPROJ",
            "base_url": "https://company.atlassian.net",
            "email": "user@company.com",
            "api_token": "your-token"
        }

        stories = await enhancer.fetch_jira_stories(config)
        print(f"Fetched {len(stories)} stories")

asyncio.run(fetch_from_jira())
```

## 🎨 Enhanced GUI Features

### Tabbed Interface
- **Story Input & Analysis**: Input stories and run AI analysis
- **AI Enhancement**: Get contextual best practices and improvements
- **PRD Generation**: Generate and enhance PRDs with AI
- **Jira/Confluence**: Direct integration with Atlassian tools

### AI-Powered Capabilities
- **Real-time Analysis**: Instant quality assessment
- **Smart Suggestions**: Context-aware improvements
- **Industry Best Practices**: Domain-specific guidance
- **Validation Checks**: Completeness verification

### Integration Features
- **Bulk Import**: Import multiple stories from Jira
- **Custom Filtering**: Use JQL for precise story selection
- **Requirements Mining**: Extract requirements from Confluence
- **Progress Tracking**: Monitor improvement progress

## 🔧 Configuration

### Domain-Specific Guidelines
The MCP server provides tailored guidance for different domains:

- **Fintech**: Compliance, security, audit trails
- **Healthcare**: HIPAA compliance, patient privacy
- **E-commerce**: Payment processing, inventory management
- **SaaS**: Multi-tenancy, subscription management
- **Mobile**: Touch interactions, offline functionality
- **Web**: Browser compatibility, responsive design

### Quality Assessment Criteria
Stories are evaluated based on:
- **Format**: Gherkin vs. free-form vs. BDD
- **Completeness**: Acceptance criteria, priority, story points
- **Clarity**: Specificity and measurability
- **INVEST Principles**: Independent, Negotiable, Valuable, Estimable, Small, Testable

## 🚨 Error Handling

The MCP server includes comprehensive error handling:
- **Connection Failures**: Graceful Atlassian API error handling
- **Invalid Input**: Input validation and user feedback
- **Rate Limiting**: Respect API rate limits
- **Authentication**: Clear error messages for auth issues

## 🔮 Future Enhancements

### Planned Features
- **Multi-language Support**: Non-English user story analysis
- **Advanced NLP**: Deeper semantic understanding
- **Integration Expansion**: Azure DevOps, GitHub, GitLab
- **Template Library**: Pre-built industry templates
- **Collaboration Features**: Team-based story refinement
- **Analytics Dashboard**: Quality trends and metrics

### API Extensions
- **Webhook Support**: Real-time Jira/Confluence updates
- **Bulk Operations**: Mass story processing
- **Custom Validators**: User-defined quality rules
- **Export Formats**: Additional output formats

## 🤝 Integration with Claude Code

This MCP server is designed to work seamlessly with Claude Code and other AI assistants:

- **Context Awareness**: Leverages conversation context for better suggestions
- **Tool Chaining**: Combines multiple tools for complex workflows
- **Iterative Refinement**: Supports multi-round improvement cycles
- **Knowledge Integration**: Incorporates best practices from industry experts

## 📚 Technical Details

### MCP Protocol Implementation
- **JSON-RPC 2.0**: Standard protocol compliance
- **Async Operations**: Non-blocking I/O for better performance
- **Resource Management**: Efficient handling of large datasets
- **Error Propagation**: Detailed error information

### Performance Optimizations
- **Connection Pooling**: Efficient API usage
- **Caching**: Reduced redundant requests
- **Batch Processing**: Optimized bulk operations
- **Memory Management**: Efficient large text handling

## 🐛 Troubleshooting

### Common Issues
1. **MCP Server Won't Start**: Check Python dependencies and permissions
2. **Atlassian Connection Failed**: Verify credentials and network access
3. **Analysis Timeout**: Check story length and complexity
4. **Import Errors**: Verify project keys and permissions

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This MCP server transforms the PRD Generator from a standalone tool into an intelligent, connected system that leverages the power of AI and integrates seamlessly with your existing development workflow.