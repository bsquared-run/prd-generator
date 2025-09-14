# PRD Generator

A sleek GUI application that parses user stories and generates comprehensive Product Requirements Documents (PRDs).

## Features

- **Modern GUI**: Clean, dark-themed interface built with CustomTkinter
- **User Story Parsing**: Supports multiple formats including Gherkin syntax
- **Automatic PRD Generation**: Creates structured PRDs with standard sections
- **Export Options**: Export to PDF and text formats
- **Project Information**: Capture project metadata and author details
- **File Loading**: Load user stories from text files

## Installation

1. Ensure Python 3.7+ is installed on your system
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python prd_generator.py
   ```

2. **Input User Stories**: Enter your user stories in the left panel. The application supports:
   - **Gherkin Format**: "As a [user], I want [functionality] so that [benefit]"
   - **Free-form text**: Any descriptive text
   - **Acceptance Criteria**: Use "Acceptance Criteria:" or "AC:" labels
   - **Priority**: Use "Priority:" or "Prio:" labels (High/Medium/Low)
   - **Story Points**: Use "Story Points:" or "SP:" labels

3. **Project Information**: Fill in project details (title, author, target release)

4. **Parse Stories**: Click "Parse User Stories" to process your input

5. **Generate PRD**: Click "Generate PRD" to create the document

6. **Export**: Use "Export as PDF" or "Export as Text" to save your PRD

## User Story Format Examples

### Gherkin Format
```
As a project manager, I want to create user accounts so that team members can access the system.
Priority: High
Story Points: 5

Acceptance Criteria:
- Users can register with email and password
- Email verification is required
- Password must meet security requirements
```

### BDD Format
```
User Authentication Feature

Given I am on the login page
When I enter valid credentials
Then I should be logged into the system
And I should see the dashboard

Priority: High
```

### Simple Format
```
The system should allow users to reset their passwords via email.

Acceptance Criteria:
- Password reset link expires after 24 hours
- Users receive email with reset instructions
- New password must meet security policy
```

## Generated PRD Sections

The application generates PRDs with the following sections:

1. **Project Information** - Basic project metadata
2. **Executive Summary** - High-level project overview
3. **Product Overview** - Vision and value proposition
4. **User Stories and Requirements** - Detailed story breakdown
5. **Functional Requirements** - System functionality requirements
6. **Acceptance Criteria** - Testable conditions for each story
7. **Assumptions and Constraints** - Project assumptions
8. **Success Metrics** - Measurement criteria

## File Structure

```
PRDGenerator/
├── prd_generator.py      # Main application file
├── requirements.txt      # Python dependencies
├── sample_user_stories.txt # Example user stories
└── README.md            # This file
```

## Dependencies

- **customtkinter**: Modern GUI framework for Python
- **reportlab**: PDF generation library

## Sample Data

Load `sample_user_stories.txt` to see example user stories and test the application functionality.

## Tips for Best Results

1. **Separate Stories**: Use blank lines to separate different user stories
2. **Include Acceptance Criteria**: Add specific, testable conditions
3. **Set Priorities**: Use High/Medium/Low to help with planning
4. **Add Story Points**: Include estimation for development planning
5. **Be Specific**: Clear, detailed stories generate better PRDs

## Troubleshooting

- **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
- **GUI Issues**: Make sure you're running Python 3.7+ with tkinter support
- **PDF Export Problems**: Verify reportlab is properly installed

## Contributing

Feel free to enhance the application by:
- Adding new export formats
- Improving parsing algorithms
- Extending PRD templates
- Adding validation features