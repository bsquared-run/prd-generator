# PRD Generator - AI-Enhanced Product Requirements Document Creator

A comprehensive system for creating professional Product Requirements Documents (PRDs) from user stories, now enhanced with AI-powered capabilities and Atlassian integration.

## 🚀 Features

### Core PRD Generator
- **Modern GUI**: Clean, dark-themed interface built with CustomTkinter
- **Advanced User Story Parsing**: Supports Gherkin syntax, acceptance criteria, priorities
- **Professional PRD Generation**: Industry-standard 8-section PRD structure
- **Multiple Export Formats**: PDF and text export capabilities
- **Template System**: Customizable PRD templates

### 🤖 AI Enhancement (MCP Integration)
- **Intelligent Story Analysis**: AI-powered quality scoring (0-100 scale)
- **Contextual Best Practices**: Domain-specific guidance (fintech, healthcare, e-commerce, etc.)
- **Story Improvement Suggestions**: AI-generated enhancement recommendations
- **PRD Validation**: Completeness checking against industry standards
- **Jira/Confluence Integration**: Direct import from Atlassian tools

## 📁 Project Structure

```
PRDGenerator/
├── prd_generator.py              # Core application (22KB)
├── enhanced_prd_generator.py     # AI-enhanced GUI (32KB)
├── requirements.txt              # Core dependencies
├── sample_user_stories.txt       # Example data
├── simple_test.py               # Basic functionality test
├── demo_simple.py               # Demo script
├── mcp-server/                  # MCP (Model Context Protocol) Server
│   ├── server.py                # MCP server implementation (28KB)
│   ├── prd_mcp_client.py        # Client integration library (11KB)
│   ├── test_mcp.py              # MCP test suite (8KB)
│   └── requirements.txt         # MCP dependencies
├── docs/                        # Documentation
│   ├── MCP_README.md           # MCP server documentation
│   ├── INTEGRATION_GUIDE.md    # Integration guide
│   └── DEVELOPMENT.md          # Development process documentation
├── examples/                    # Usage examples
└── LICENSE                     # MIT License
```

## 🎯 Quick Start

### Option 1: Basic PRD Generator
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python prd_generator.py
```

### Option 2: AI-Enhanced Version
```bash
# Install core dependencies
pip install -r requirements.txt

# Install MCP dependencies
pip install -r mcp-server/requirements.txt

# Run enhanced application
python enhanced_prd_generator.py
```

## 🤖 MCP Server (AI Enhancement)

The MCP (Model Context Protocol) server provides AI-powered enhancements:

### Available Tools
1. **`fetch_jira_stories`** - Import stories from Jira projects
2. **`analyze_user_story`** - AI quality assessment and scoring
3. **`improve_user_stories`** - Generate improvement suggestions
4. **`get_best_practices`** - Contextual writing guidance
5. **`enhance_prd_content`** - AI-powered PRD enhancement
6. **`validate_prd_completeness`** - Industry standard validation
7. **`fetch_confluence_requirements`** - Extract requirements from Confluence

### Start MCP Server
```bash
cd mcp-server
python server.py
```

### Test MCP Integration
```bash
cd mcp-server
python test_mcp.py
```

## 📝 Usage Examples

<img width="1736" height="1154" alt="image" src="https://github.com/user-attachments/assets/4170ee6c-10f6-4173-a7e2-da5fa76b54b9" />

### Basic Workflow
1. **Enter User Stories**: Input stories in Gherkin or free-form format
2. **Parse Stories**: Extract structured data and metadata
3. **Generate PRD**: Create professional documentation
4. **Export**: Save as PDF or text

### Enhanced AI Workflow
1. **Import from Jira**: Connect and bulk import stories
2. **AI Analysis**: Get quality scores and improvement suggestions
3. **Apply Best Practices**: Use domain-specific guidance
4. **Generate Enhanced PRD**: AI-validated professional output
5. **Validate & Export**: Quality-assured final documentation

### Sample User Story Formats

#### Gherkin Format
```
As a project manager, I want to create user accounts so that team members can access the system.
Priority: High
Story Points: 5

Acceptance Criteria:
- Users can register with email and password
- Email verification is required
- Password must meet security requirements
```

#### BDD Format
```
Given I am on the login page
When I enter valid credentials
Then I should be logged into the system
And I should see the dashboard

Priority: High
```

## 🔗 Integrations

### Jira Integration
- **Project Import**: Bulk import stories using JQL queries
- **Metadata Preservation**: Maintains priorities, story points, labels
- **Custom Fields**: Supports Jira custom field mapping
- **Authentication**: Secure API token-based authentication

### Confluence Integration
- **Requirements Extraction**: Pull requirements from documentation
- **Page Content Analysis**: Process structured and unstructured content
- **Space-level Import**: Import from entire Confluence spaces
- **Content Filtering**: Query-based page selection

### AI Assistant Integration
- **MCP Protocol**: Standard integration with AI assistants
- **Claude Code Compatible**: Seamless integration with Claude Code
- **Tool Chaining**: Combine multiple AI operations
- **Context Preservation**: Maintain conversation context

## 🏗️ Architecture

### Core Application
```
User Input → Story Parser → PRD Generator → Export Engine
```

### AI-Enhanced System
```
Jira/Confluence → AI Analysis → Enhanced Parser → Smart PRD Generator → Validated Export
      ↑              ↑               ↑                    ↑                  ↑
   MCP Tools    Quality Scoring   Best Practices    AI Enhancement    Quality Validation
```

## 📊 Quality Metrics

### Story Quality Assessment
- **Format Compliance**: Gherkin/BDD structure adherence (30 points)
- **Acceptance Criteria**: Presence and quality of testable conditions (25 points)
- **Clarity & Specificity**: Clear, unambiguous language (20 points)
- **Business Value**: Clear value proposition and benefits (15 points)
- **Testability**: Measurable success criteria (10 points)

### PRD Completeness Standards
- **Agile Standard**: Product Vision, User Stories, Acceptance Criteria, Success Metrics
- **Enterprise Standard**: Executive Summary, Business Requirements, Risk Assessment
- **Custom Standards**: Configurable validation rules

## 🎨 Screenshots & Demo

### Core Application Interface
- Clean, modern dark-themed GUI
- Two-panel layout (input/output)
- Real-time parsing feedback
- Export options (PDF/Text)

### Enhanced AI Interface
- Tabbed workflow organization
- AI analysis dashboard
- Best practices sidebar
- Integration management panel

## 🔧 Development

### Core Dependencies
- **CustomTkinter**: Modern GUI framework
- **ReportLab**: Professional PDF generation
- **Python 3.7+**: Core runtime

### MCP Dependencies
- **MCP Protocol**: Model Context Protocol implementation
- **Requests**: HTTP client for API integration
- **Asyncio**: Asynchronous operation support

### Testing
```bash
# Test core functionality
python simple_test.py

# Test MCP integration
cd mcp-server && python test_mcp.py

# Run demo
python demo_simple.py
```

## 🌟 Industry Applications

### Fintech
- Compliance requirement tracking
- Security and audit trail specifications
- Regulatory adherence validation
- Multi-currency considerations

### Healthcare
- HIPAA compliance integration
- Patient privacy requirements
- Clinical workflow specifications
- Accessibility considerations

### E-commerce
- Payment processing requirements
- Inventory management integration
- Multi-platform consistency
- User account management

### SaaS
- Multi-tenant architecture considerations
- Subscription and billing requirements
- User role and permission management
- Scalability specifications

## 📈 Roadmap

### Current Version (v1.0)
- ✅ Core PRD generation
- ✅ User story parsing
- ✅ PDF/Text export
- ✅ MCP server integration
- ✅ Jira/Confluence connectivity

### Next Release (v1.1)
- 🔄 Enhanced NLP analysis
- 🔄 Additional export formats
- 🔄 Template customization
- 🔄 Batch processing improvements

### Future Vision (v2.0)
- 🎯 Predictive story complexity analysis
- 🎯 Automated test case generation
- 🎯 Multi-language support
- 🎯 Advanced analytics dashboard

## 🤝 Contributing

We welcome contributions! Key areas for development:

1. **New Integrations**: Azure DevOps, GitHub, GitLab
2. **Enhanced AI**: Improved analysis algorithms
3. **UI/UX**: Interface enhancements and themes
4. **Export Formats**: Word, Confluence, etc.
5. **Templates**: Industry-specific PRD templates

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/bsquared-run/prd-generator
- **Issues**: https://github.com/bsquared-run/prd-generator/issues
- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)

## 🙏 Acknowledgments

- **Research Foundation**: Atlassian, ProductPlan, and Wikipedia PRD standards
- **AI Enhancement**: Built with Claude Code integration in mind
- **Community**: Open source contributors and product management community

---

**Transform your user stories into professional Product Requirements Documents with AI-powered intelligence and seamless development tool integration.**
