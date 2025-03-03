# AI Development Process Prompts

## Practical Workflow Guide
```markdown
Key Timing Considerations:
1. Starting Work:
   - Write clear prompts
   - Include full context
   - Be specific

2. During Processing:
   - Let AI "cook" - be patient
   - Take a coffee break
   - Work on other tasks
   - Review documentation
   - Plan next steps

3. Review Process:
   - Check periodically
   - Review carefully
   - Test thoroughly
   - Verify changes

IMPORTANT: Never rush AI processing. Use waiting time effectively.
```

## Implementation Template
```markdown
1. What We're Doing:
   [2-4 sentences explaining the task]

2. Relevant Files:
   [Tag all immediately relevant files]

3. Execution Instructions:
   - How to proceed
   - What to avoid
   - Specific requirements
   - DO NOT STOP WORKING until complete

4. Context Dump:
   [Include relevant documentation/context]

5. Core Instruction:
   [Repeat main request]

6. Output Format:
   - Clean, maintainable code
   - Comprehensive comments
   - Error handling
   - Tests

IMPORTANT: The fewer lines of code, the better
```

## Error Analysis Process
```markdown
We have an error in [file/component].

IMPORTANT: Start with uncertainty and write three paragraphs:

1. Initial Assessment:
   - Observed symptoms
   - Occurrence patterns
   - Environmental factors

2. Context Analysis:
   - Related systems
   - Recent changes
   - Configuration factors

3. Potential Causes:
   - Multiple possibilities
   - Likelihood analysis
   - Investigation priorities

Only after analysis:
1. Propose debugging steps
2. Request needed information
3. Suggest potential solutions

Remember: Build confidence through systematic analysis
```

## Solution Comparison
```markdown
Write two detailed paragraphs for each solution:

Solution 1: [First approach]
[Thoroughly analyze benefits and considerations]

Solution 2: [Second approach]
[Thoroughly analyze benefits and considerations]

Start uncertain, then build confidence.

After consideration:
1. Which solution is better (if any)
2. Specific reasons why
3. Trade-offs considered
4. Implementation implications

====

Remember: Consider multiple approaches before deciding
```

## MVP Analysis Template
```markdown
Let's analyze this feature with MVP approach:

1. Core Value Analysis:
   - What problem does this solve?
   - Who needs this urgently?
   - What solves 80% with 20% effort?

2. Feature Breakdown:
   Essential (Must have):
   - Core functionality
   - Basic requirements
   - Immediate value
   
   Nice to Have (Can wait):
   - Enhancements
   - Future improvements
   - Additional capabilities
   
   Not MVP (Exclude):
   - Pure enhancements
   - Deferred features
   - Nice-to-have items

3. Implementation Strategy:
   - Clear scope boundaries
   - Explicit exclusions
   - Completion criteria
   - Scope creep risks

4. Validation Criteria:
   - MVP sufficiency metrics
   - Success indicators
   - User feedback needs

IMPORTANT: Perfect is the enemy of good enough
```

## Technical Debt Assessment
```markdown
Before implementation, assess debt:

1. Understanding Check:
   - Full component understanding?
   - Knowledge gaps?
   - Documentation sufficient?

2. Implementation Risks:
   - Current assumptions
   - Future change likelihood
   - Coupling concerns
   - Performance implications

3. Documentation Needs:
   - Required documentation
   - Needed comments
   - Special considerations
   - Known limitations

4. Mitigation Strategy:
   - How to minimize debt
   - Documentation plan
   - Testing approach
   - Maintenance considerations

IMPORTANT: Have clear debt prevention plan
```

## Documentation Structure
```markdown
# Specialized Documentation Files

## Database Setup (database.md)
- Table structures
- Relationships
- Access policies
- Required fields
- Default values
- SQL queries

## Design Principles (design.md)
- UI/UX guidelines
- Component patterns
- Style conventions
- Layout principles

## API Documentation (api.md)
- Endpoint specifications
- Request/response formats
- Authentication requirements
- Rate limits

## Environment Variables
DATABASE_URL=
API_KEY=
[etc.]

## File Structure
```
[Generated using `tree` command]
```
```

## Web Search Integration
```markdown
Create one-paragraph search query:
- Include all context
- Specify versions
- Request technical details
- Focus on current practices

CAUTION - Watch for:
- Outdated solutions
- Incorrect implementations
- Mismatched versions
- Poor practices

After results:
1. Write three analysis paragraphs
2. Identify red herrings
3. Focus on relevant info
4. Verify against context
5. Cross-reference docs

IMPORTANT: Verify before implementing
```

## Composer Context Switch
```markdown
Before switching, summarize:

1. Recent Changes:
   - Implemented changes
   - Updated files
   - Change purposes

2. Implementation Status:
   - Working features
   - Failed attempts
   - Abandoned approaches

3. Current Limitations:
   - Known bugs
   - Performance issues
   - Technical debt

4. Essential Context:
   - Dependencies
   - Constraints
   - Key decisions
   - Required knowledge

5. Next Steps:
   - Planned changes
   - Required fixes
   - Future work

IMPORTANT: Document everything needed
```

====

IMPORTANT: Follow these prompts consistently.
Remember: Take time to analyze first.
Focus: Quality over speed.
--------------------------------------------------------------------------------
# Universal PRD Generation Prompt

I'm planning to build [PROJECT_NAME], which is a [PROJECT_TYPE: Frontend/Backend/Mobile/Fullstack] application. The core purpose is [BRIEF_DESCRIPTION]. Help me create a comprehensive PRD that includes all necessary technical specifications and requirements.

Key functionalities include: [LIST_KEY_FEATURES]

The PRD should be structured to address all relevant technical aspects while remaining clear and unambiguous for the development team.

## Project Type Specifications

Please specify the project type:

### Frontend Development
- Framework/library requirements
- UI/UX specifications
- State management approach
- Responsive design requirements
- Browser compatibility

### Backend Development
- Server architecture
- Database requirements
- API design patterns
- Authentication/Authorization
- Scalability considerations

### Mobile Development
- Platform specifications (iOS/Android)
- Device compatibility
- Native features usage
- Performance requirements
- Store deployment considerations

### Fullstack Development
- System architecture
- Service integration
- Data flow patterns
- Development stack
- Deployment strategy

## Required Information

Please provide:
1. Project Basics
   - Project name and type
   - Core objectives
   - Target users/audience
   - Key features
   - Technical constraints

2. Technical Context
   - Development stack preferences
   - Infrastructure requirements
   - Integration needs
   - Scalability expectations
   - Performance requirements

3. Feature Details
   - Functionality descriptions
   - User interactions
   - Technical requirements
   - Integration points
   - Data handling needs

4. Integration Requirements
   - External services
   - APIs
   - Authentication
   - Data storage
   - Third-party tools

## PRD Structure

The output should follow this format:

```markdown
# [Project Name] Product Requirements Document

## 1. Project Overview
- Purpose and Scope
- System Context
- Technical Architecture
- Development Approach

## 2. System Requirements
### 2.1 Technical Stack
- Frontend Technologies
- Backend Systems
- Databases
- External Services

### 2.2 Architecture Overview
- System Components
- Data Flow
- Integration Points
- Security Considerations

## 3. Feature Requirements
### 3.1 [Feature 1]
- Functional Description
- Technical Requirements
- Implementation Details
- Integration Needs
- Dependencies

[Additional features numbered sequentially]

## 4. Data Specifications
### 4.1 Data Models
- Entity Definitions
- Relationships
- Validation Rules
- Storage Requirements

### 4.2 API Contracts
- Endpoint Specifications
- Request/Response Formats
- Authentication Methods
- Error Handling
- Usage Examples

## 5. Technical Requirements
### 5.1 Development Requirements
- Environment Setup
- Tool Requirements
- Coding Standards
- Documentation Needs

### 5.2 Performance Requirements
- Load Handling
- Response Times
- Scalability Metrics
- Resource Usage

### 5.3 Security Requirements
- Authentication
- Authorization
- Data Protection
- Compliance Needs

## 6. Development Considerations
- Testing Strategy
- Deployment Approach
- Monitoring Plan
- Maintenance Requirements
```

## Additional Elements

The PRD should include:
1. Numbered requirements
2. Clear technical specifications
3. Implementation examples
4. Integration patterns
5. Error handling approaches
6. Testing requirements
7. Deployment considerations

## Project-Specific Sections

Based on project type, include relevant sections:

### Frontend Focus
- UI Component Specifications
- State Management Patterns
- Route Definitions
- Asset Requirements
- Build Configuration

### Backend Focus
- API Specifications
- Database Schema
- Service Architecture
- Caching Strategy
- Security Measures

### Mobile Focus
- Platform Guidelines
- Native Features
- Offline Capabilities
- Performance Optimization
- Store Requirements

### Fullstack Focus
- System Architecture
- Service Integration
- Development Workflow
- Deployment Pipeline
- Monitoring Strategy

## Validation Checklist

Ensure the PRD includes:
- Complete technical specifications
- Clear implementation guidelines
- Explicit integration requirements
- Comprehensive error handling
- Performance criteria
- Security considerations
- Testing approach
- Deployment strategy

## Response Format

When generating the PRD:
1. Identify project type and scope
2. Address relevant technical aspects
3. Include platform-specific considerations
4. Provide implementation examples
5. Specify validation criteria
6. List assumptions and constraints
7. Highlight risk areas
8. Suggest next steps

## Implementation Notes

Use this prompt with advanced language models to generate comprehensive PRDs. Adjust detail level based on:
- Project complexity
- Team expertise
- Development timeline
- Technical requirements
--------------------------------------------------------------------------------
# Development Process-Specific Prompts

## Initial Project Setup

```markdown
Help me set up a [project type] project with the following requirements:
- Core functionality: [description]
- Technical stack: [list of technologies]
Please create:
1. Project structure documentation
2. Core functionality documentation
3. Required dependencies list
4. Initial setup instructions
```

## Feature Implementation

```markdown
Let's implement [feature name] based on the provided documentation:
1. Current file structure: [structure]
2. Feature requirements: [requirements]
3. Dependencies used: [dependencies]
Please implement this feature maintaining existing patterns and documentation.
```

## Error Resolution

```markdown
I encountered this error while implementing [feature]:
[error details]

Current implementation:
[relevant code]

Please help:
1. Identify root cause
2. Suggest solution
3. Prevent similar issues
```

## UI Enhancement

```markdown
Please improve the UI of [component] while maintaining functionality:
- Current implementation: [code]
- Desired improvements: Better visual design, consistent styling
- Constraints: Maintain all existing functionality and variables
```

## Documentation Creation

```markdown
Create detailed documentation for [project/feature] including:
1. Project overview
2. Core functionalities
- [functionality 1]
- [functionality 2]
3. File structure
4. Technical requirements
5. Implementation steps
```

## Backend Integration

```markdown
Help integrate [backend service] with current implementation:
1. Current project structure: [structure]
2. Required functionality: [requirements]
3. Data schema: [schema details]
Please provide:
- Integration steps
- Schema updates
- API implementation
```

## Component Development

```markdown
Create a [component type] with these requirements:
1. Functionality: [description]
2. Props/Parameters: [list]
3. Integration points: [details]
Please implement maintaining project patterns and documentation.
```

## Testing Implementation

```markdown
Help implement tests for [feature/component]:
1. Current implementation: [code]
2. Test requirements:
- Functionality verification
- Error handling
- Edge cases
Please provide comprehensive test coverage.
```

## Performance Optimization

```markdown
Help optimize [feature/component] performance:
1. Current implementation: [code]
2. Performance issues: [description]
3. Constraints: [list]
Please suggest and implement optimizations.
```

## Deployment Setup

```markdown
Help prepare [project] for deployment:
1. Current setup: [details]
2. Target platform: [platform]
3. Requirements:
- Environment configuration
- Build optimization
- Deployment procedures
```
--------------------------------------------------------------------------------
# Project Structure Creation Prompt

Above is the project I want to build. Help me structure my project files in a way that:
- Creates as few files as possible to minimize complexity and potential errors
- Maintains clear organization and separation of concerns
- Follows best practices for the chosen technology stack
- Enables efficient development and maintenance

Please analyze the requirements step by step:

1. Core Functionality Analysis
- Identify the main features and their dependencies
- Determine shared functionality
- Identify potential reusable components
- Map out data flow requirements

2. Technical Requirements Analysis
- Review the technology stack requirements
- Identify necessary configuration files
- Determine required directory structure for the chosen framework
- Consider build and deployment requirements

3. File Organization Guidelines
- Group related functionality together
- Minimize nesting levels
- Keep configuration separate from implementation
- Consider scalability and maintainability

4. Optimization Considerations
- Consider code splitting opportunities
- Plan for lazy loading where appropriate
- Account for testing requirements
- Consider build optimization needs

Based on this analysis, please provide:

1. A complete directory tree structure showing:
- All necessary directories
- Key files with their purposes
- Configuration files
- Component organization

2. Brief explanations for:
- The purpose of each major directory
- Key file responsibilities
- Organization rationale
- Implementation considerations

3. Development guidelines including:
- File naming conventions
- Import/export patterns
- State management approach
- Data flow patterns

The goal is to create a minimal yet complete project structure that:
- Supports all required functionality
- Maintains clear organization
- Minimizes complexity
- Enables efficient development
- Follows framework best practices

Remember to use the tree command format for the directory structure:
```
project-root/
├── directory1/
│   ├── file1.ext
│   └── file2.ext
└── directory2/
    └── file3.ext
```

Please ensure the structure is minimal while meeting all project requirements.
--------------------------------------------------------------------------------
# PRD Creation and Enhancement Prompt

Please help create/enhance a detailed Product Requirements Document (PRD) that provides clear alignment for developers implementing this project. Follow these guidelines:

## Analysis Steps

1. Initial Requirements Processing
- Review provided project description
- Identify core functionalities
- List technical requirements
- Note any constraints or limitations

2. Documentation Structure
Organize the PRD into these key sections:

### Project Overview
- Clear project description
- Core objectives
- Target users/audience
- Success criteria

### Technical Requirements
- Technology stack details
- External dependencies
- API requirements
- Development environment needs

### Functional Specifications
- Detailed feature descriptions
- User interactions
- Data flow requirements
- Integration points

### Implementation Guidelines
- Coding standards
- Architecture patterns
- Performance requirements
- Security considerations

## Required Components

1. Project Structure
```
[Project Name]
├── Directory structure
│   ├── Key files
│   └── Configuration files
└── Implementation files
```

2. Code Examples
```typescript
// Example implementations
// Function signatures
// API calls
// Component structures
```

3. Expected Responses
```json
{
    "example": "response format",
    "status": "success/error cases"
}
```

4. Integration Examples
```typescript
// API integration patterns
// External service connections
// Authentication flows
```

## Documentation Requirements

1. Feature Documentation
- Detailed description
- User interaction flows
- Technical requirements
- Implementation considerations
- Testing requirements

2. Technical Documentation
- API specifications
- Database schemas
- Authentication flows
- Integration points

3. Implementation Examples
- Code snippets
- Configuration examples
- Usage patterns
- Error handling

4. Development Guidelines
- Setup instructions
- Coding standards
- Testing requirements
- Deployment procedures

## Important Considerations

1. Clarity
- Use clear, unambiguous language
- Provide specific examples
- Include all necessary context
- Define technical terms

2. Completeness
- Cover all features
- Include error cases
- Document edge cases
- Specify all requirements

3. Practicality
- Focus on implementable solutions
- Include realistic examples
- Consider development constraints
- Account for maintenance needs

4. Alignment
- Ensure consistency with project goals
- Maintain technical feasibility
- Consider scalability needs
- Account for future growth

## Output Format

The enhanced PRD should:
1. Follow Markdown format
2. Use consistent heading levels
3. Include code blocks where appropriate
4. Maintain clear section separation

## Final Verification

Ensure the PRD includes:
- [ ] Complete feature descriptions
- [ ] Technical requirements
- [ ] Implementation examples
- [ ] Code snippets
- [ ] Expected responses
- [ ] File structure
- [ ] Setup instructions
- [ ] Development guidelines

Remember:
- Focus on clarity and completeness
- Provide practical, implementable specifications
- Include all necessary context
- Maintain consistent documentation structure
--------------------------------------------------------------------------------
# Development Phase-Specific Prompts

## Project Setup Phase

```markdown
Help me set up a new [framework] project with the following requirements:
- Project name: [name]
- Core dependencies: [list]
- UI framework: [framework]
- Additional libraries: [list]

Please include:
1. Initial project structure
2. Configuration files
3. Required dependency installations
```

## Frontend Development Phase

```markdown
Based on the provided requirements, help me build the frontend components:

Reference files:
- Requirements: [file path]
- UI Design: [file path/screenshot]

Focus areas:
1. Component structure
2. State management
3. User interactions
4. Error handling
5. Loading states
```

## Backend Integration Phase

```markdown
Help me implement the backend features based on the requirements:

Database Schema:
[Include table definitions]

Required Functionality:
1. [List specific functions]
2. [Include API endpoints]

Please implement:
1. Database connections
2. API routes
3. Error handling
4. Data validation
```

## Authentication Implementation Phase

```markdown
Help me implement user authentication with [service]:

Requirements:
1. User flow requirements
2. Database schema updates
3. Protected routes
4. User profile management

Integration points:
1. Frontend components
2. Backend routes
3. Middleware setup
```

## Deployment Preparation Phase

```markdown
Help me prepare the application for deployment:

Environment:
- Platform: [platform]
- Requirements: [list]

Tasks:
1. Environment variable setup
2. Build configuration
3. Error handling
4. Performance optimization
```

## Error Resolution Template

```markdown
I got this error:
[Error message]

Please help me:
1. Analyze root cause
2. Provide step-by-step resolution
3. Suggest prevention measures
```

## Notes
- Adapt prompts based on specific project needs
- Include relevant file paths and screenshots
- Maintain consistent structure across phases
- Always include error handling requirements
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
# Process-Specific Prompt Templates

## Feature Implementation Prompts

### Initial Setup Template
```markdown
Create a new [framework] project with the following specifications:
- Framework: [framework name]
- Key features: [list key features]
- Required dependencies: [list dependencies]
Start by setting up the basic project structure and installing necessary packages.
```

### Component Development Template
```markdown
Develop a [component name] with the following requirements:
- Functionality: [describe functionality]
- Dependencies: [list dependencies]
- User interactions: [describe interactions]

Reference files:
[List relevant files]

Visual reference: [Attach screenshot if applicable]
```

### Error Resolution Template
```markdown
When attempting [action], encountering error:
[Error details]

Additional context:
- Relevant file: [filename]
- Current behavior: [description]
- Expected behavior: [description]
- Screenshot: [if applicable]

Implement the fix in the simplest way possible with minimal code changes.
```

## Code Modification Templates

### Feature Addition
```markdown
Add [feature] to [component/file] with these requirements:
1. Functionality: [description]
2. Integration points: [list]
3. Error handling: [requirements]
4. Visual references: [screenshots]

Focus on [specific file] for implementation.
```

### Bug Fix
```markdown
Fix issue in [component/file]:
1. Current behavior: [description]
2. Expected behavior: [description]
3. Error messages: [if any]
4. Visual reference: [screenshot]

Make changes as minimal as possible while ensuring proper fix.
```

### Code Refactoring
```markdown
Refactor [component/file] to:
1. Improve [specific aspect]
2. Maintain current functionality
3. Focus on [specific area]
4. Ensure backwards compatibility

Target files: [list files]
```

## Integration Templates

### API Integration
```markdown
Implement [API name] integration:
1. Endpoint: [endpoint details]
2. Authentication: [requirements]
3. Data handling: [specifications]
4. Error cases: [list scenarios]

Focus on creating robust error handling.
```

### Component Connection
```markdown
Connect [component A] with [component B]:
1. Data flow: [description]
2. Event handling: [requirements]
3. Error scenarios: [list]
4. Visual feedback: [requirements]

Include screenshots of expected behavior if available.
```

## Best Practices for Prompt Usage

1. **Provide Clear Context**
   - Reference specific files
   - Include relevant screenshots
   - Describe current and expected behavior

2. **Specify Scope**
   - List affected files
   - Define clear boundaries
   - Indicate priority aspects

3. **Include Visual References**
   - Add screenshots for UI components
   - Provide mockups when available
   - Reference existing similar features

4. **Error Handling**
   - Describe error scenarios
   - Specify required validations
   - Define recovery procedures

5. **Implementation Guidelines**
   - Request minimal necessary changes
   - Focus on specific files/components
   - Prioritize simplicity in solutions
--------------------------------------------------------------------------------
# Complete Process-Specific Prompts Collection

## Input Method Prompts

### Voice Input (Whisper Flow)
```markdown
[Activate Whisper Flow]
Speak clearly and structured:
- Feature requirements
- Implementation details
- Context information
- File references
Note: Optimal for 200+ words/minute input
```

### Text Input
```markdown
[For precise operations]
- Code snippets
- File edits
- Exact syntax
- Short commands
```

## Implementation Prompts

### Minimal Code Implementation
```markdown
[Feature description]
Requirements:
- The fewer lines of code the better
- Proceed like a senior developer
- Focus on core functionality
- Keep it simple and clean
```

### Complex Feature Development
```markdown
[Feature details]
Instructions:
- Do not stop working until you've implemented this feature fully and completely
- Only include the truly necessary steps
- Follow best practices
- Write comprehensive tests
```

### Error Resolution
```markdown
We have an error in [filename].
Process:
1. Start by writing three reasoning paragraphs analyzing what the error might be
2. Do not jump to conclusions
3. Consider all potential causes
4. Propose solution strategy
```

### Unbiased Solution Comparison
```markdown
Before you answer, I want you to:
1. Write two detailed paragraphs
2. One arguing for each solution
3. Do not jump to conclusions
4. Seriously consider both approaches
5. After completion, identify the superior solution with clear reasoning
```

### Uncertainty-First Analysis
```markdown
Start reasoning with uncertainty:
1. Begin with possibilities and questions
2. Gradually build confidence through analysis
3. Consider multiple perspectives
4. Arrive at well-reasoned conclusions
```

## Web Integration Prompts

### Search Query Formation
```markdown
Your task is to write a one-paragraph search query:
- Format as instructions to a human researcher
- Include all relevant context
- Specify needed code snippets/technical details
- Focus on current documentation needs
```

### Search Results Processing
```markdown
Give me the TLDR of the search results.
Important:
- Be careful of dangerous and distracting red herrings
- Focus on relevant information
- Verify currency of information
- Cross-reference with known facts
```

## Context Management Prompts

### State Summary Request
```markdown
Before we proceed, provide a summary of:
1. Recent actions taken
2. Failed attempts
3. Updated files
4. Current project state
5. Next steps needed
Note: Include only verified facts, no assumptions
```

### File Context
```markdown
File: [complete path/to/file]
Location: [project structure]
Purpose: [file's role]
Content: [relevant code]
Dependencies: [related files]
```

## Specialized Tool Integration

### V0 Design Integration
```markdown
Converting design to implementation:
1. List all components
2. Specify styling requirements
3. Note interactions
4. Define data requirements
5. Identify dependencies
```

### Database Schema Management
```markdown
For [database_type]:
1. Table definitions
2. Relationships
3. Constraints
4. Access policies
5. Migration plans
Reference: database.md
```

## Model Selection Prompts

### Primary Model Usage
```markdown
Using Claude 3.5 Sonnet 1022:
- Complex implementations
- Multi-file changes
- Reasoning tasks
- Documentation generation
```

### Alternative Model Selection
```markdown
Switch to [alternative model] for:
- New perspective needed
- Specific capabilities required
- Primary model limitations
- API issues
```

## Debug Assistance Prompts

### Debugging Guide Request
```markdown
Experience Level: [beginner/intermediate/advanced]
Technology: [specific tech]
Tool: [debugging tool]
Request: Step-by-step debugging instructions
Focus: Gathering relevant context
```

### Context Gathering
```markdown
As a senior developer, need:
1. Error details
2. System state
3. Recent changes
4. Environment info
5. Reproduction steps
Provide step-by-step context gathering instructions
```
--------------------------------------------------------------------------------
# Process-Specific Development Prompts

## PRD Development Prompts

### Initial Draft PRD
```markdown
Please help me create a draft Process Requirements Document (PRD) for [application name]. The PRD should include:

1. Project Overview
   - Brief description of the application
   - Key workflow overview
   - Technical stack specifications

2. Core Functionalities
   - User authentication process
   - Main feature implementations
   - Data management approach
   - Technical requirements

3. Documentation Requirements
   - API specifications
   - Package dependencies
   - Integration requirements

Please structure the response in markdown format and focus on creating a foundation for further refinement.
```

### Package Research Prompt
```markdown
Based on the draft PRD for [application name], please help identify and document:

1. Required core packages for:
   - Frontend framework implementation
   - UI component libraries
   - Authentication services
   - API integrations
   - Development tools

2. Version compatibility requirements
3. Integration considerations
4. Performance implications

Please provide specific package recommendations with justification for each choice.
```

### Project Structure Prompt
```markdown
Using the current PRD and package recommendations for [application name], please help define:

1. Optimal file organization using minimal necessary files
2. Component structure
3. Configuration file requirements
4. Development environment setup

Please use the tree command format for visualization and focus on maintainable architecture.
```

### Final PRD Refinement
```markdown
Please help refine the current PRD for [application name] by:

1. Incorporating the defined project structure
2. Adding detailed implementation requirements
3. Specifying development workflows
4. Including error handling requirements
5. Defining testing criteria

Please maintain markdown formatting and ensure comprehensive documentation.
```

## Development Workflow Prompts

### Frontend Development
```markdown
Based on the PRD for [application name], please help implement:

1. Required frontend components using [framework]
2. Authentication integration with [service]
3. UI implementation using [component library]
4. State management setup

Please provide step-by-step guidance and include error handling.
```

### Backend Integration
```markdown
Following the PRD specifications for [application name], please assist with:

1. API endpoint implementation
2. Database connection setup
3. Authentication service integration
4. Environment configuration

Please include security considerations and best practices.
```

### Testing and Debugging
```markdown
For the current implementation of [application name], please help with:

1. Functionality testing
2. Error identification
3. Performance optimization
4. Security validation

Please provide specific test cases and debugging steps.
```

### Deployment Preparation
```markdown
To prepare [application name] for deployment, please assist with:

1. Environment configuration
2. Build optimization
3. Security checks
4. Deployment documentation

Please include necessary commands and configurations.
```

## Error Resolution Prompts

### Code Error Resolution
```markdown
Regarding the error in [application name]:

1. Error message: [paste error]
2. Current implementation: [relevant code]
3. Expected behavior: [description]

Please help identify the cause and provide a solution.
```

### Integration Error Resolution
```markdown
For the integration issue in [application name]:

1. Integration point: [description]
2. Current behavior: [description]
3. Expected outcome: [description]
4. Related configurations: [details]

Please help resolve the integration problem.
```

### Performance Optimization
```markdown
To improve performance in [application name]:

1. Current performance metrics: [details]
2. Problem areas: [description]
3. Target improvements: [metrics]

Please provide optimization recommendations.
```
--------------------------------------------------------------------------------
# Process-Specific Prompts for Development Workflows

## 1. Initial Planning and Visualization

```markdown
I need to plan a [project type] with the following requirements: [requirements list].
Please help me:
1. Identify the key components and their relationships
2. Suggest appropriate technologies and frameworks
3. Create a basic system architecture
4. Outline the development phases
Please consider [specific constraints] in your recommendations.
```

## 2. Technology Stack Setup

```markdown
I'm building with [technology stack]. Please:
1. Verify the compatibility of selected technologies
2. Suggest essential dependencies and configurations
3. Provide a cursor.directory compatible setup prompt
4. Outline initial project structure
Base recommendations on current best practices and official documentation.
```

## 3. Documentation Integration

```markdown
For my [technology] project, I need to:
1. Access and integrate relevant documentation
2. Set up documentation references in the development environment
3. Identify key sections for implementation guidance
4. Create a documentation-first development approach
Please focus on [specific feature/component].
```

## 4. Implementation Support

```markdown
I'm implementing [feature/component]. Please help with:
1. Code structure and organization
2. Best practices implementation
3. Error handling and edge cases
4. Performance optimization
Consider [specific requirements/constraints] in the solution.
```

## 5. Debugging and Problem-Solving

```markdown
I'm encountering [issue/error] when [context].
Previous attempted solutions:
1. [Solution 1]
2. [Solution 2]
Expected behavior: [description]
Current behavior: [description]
Please suggest alternative approaches and debugging strategies.
```

## 6. Code Explanation and Learning

```markdown
Please explain this code section:
[code block]
Focus on:
1. Overall flow and logic
2. Key concepts and patterns
3. Implementation details
4. Potential improvements
Explain as if teaching a beginner developer.
```

## 7. Cross-AI Collaboration

```markdown
Previous assistant attempted [task] with:
Approach: [description]
Result: [outcome]
Issues: [description]
Please provide a fresh perspective and alternative solutions.
Consider [specific constraints/requirements].
```

## Usage Guidelines

1. Customize prompts based on specific project needs
2. Include relevant context and constraints
3. Reference previous interactions when building upon solutions
4. Maintain consistency in communication style
5. Focus on learning and understanding, not just implementation
--------------------------------------------------------------------------------
# Process-Specific Development Prompts

## Voice Brainstorming Prompt
```markdown
I'm building [application type] to help [target users] with [specific problem].
Please:
1. Listen to my requirements and ideas
2. Help refine the concept
3. Provide creative encouragement (optional: in a specific accent/style)
4. Guide initial brainstorming session
Note: Use GPT-4 for this initial planning phase
```

## Roadmap Generation Prompt
```markdown
Based on our discussion about [application name], please:
1. Summarize the core application features
2. Create a detailed roadmap in markdown format covering:
   - Project setup
   - Core functionality implementation
   - UI/UX development
   - Testing and deployment
3. Break down each phase into clear, actionable steps
Note: Use GPT-4 Turbo (01-preview) for detailed planning
```

## Tech Stack Selection Prompt
```markdown
For [application name] with the roadmap provided above:
1. Recommend the optimal tech stack for:
   - Frontend development
   - Backend implementation
   - Database solutions
   - Authentication methods (including OAuth if needed)
   - Additional tools and services
2. Provide step-by-step development instructions
3. Include best practices and implementation guidelines
4. Specify cloud hosting requirements (Linode/Akamai)
```

## Component Development Prompt
```markdown
Help me build [component name] for [application name]:
1. The component should [description of functionality]
2. Use [specific technology/framework]
3. Include API integration (with documentation URL)
4. Follow best practices for:
   - Code organization
   - Error handling
   - Performance optimization
   - Documentation
```

## Styling and Enhancement Prompt
```markdown
Help improve the design of [component/page name]:
1. Current implementation: [paste code]
2. Desired improvements:
   - Visual enhancement
   - Responsive design
   - Dark mode support
   - Performance optimization
3. Use v0 for design generation
4. Implement styling with provided code
```

## Branding Elements Prompt
```markdown
Help create branding elements for [application name]:
1. Logo requirements:
   - Style: [description]
   - Colors: [preferences]
   - Usage context: [where it will be used]
2. Use Midjourney with specific prompts:
   - "logo [application name]"
   - "logo vector [application name]"
3. Implement selected design in application
```

## Docker Configuration Prompt
```markdown
Create Docker configuration for [application]:
1. Generate:
   - docker-compose.yaml
   - Dockerfile(s)
2. Include:
   - Development environment
   - Production setup
   - Build instructions
3. Optimize for Linode deployment
```

## Deployment Configuration Prompt
```markdown
Help configure deployment for [application]:
1. Linode/Akamai setup:
   - OS: Debian 11
   - Region: [specify]
   - Plan: Basic ($5/month)
2. Include:
   - Server configuration
   - Security settings
   - SSL setup
   - Monitoring configuration
```

## Feedback Implementation Prompt
```markdown
Based on user feedback about [feature/component]:
1. Current behavior: [description]
2. Desired behavior: [description]
3. Help implement changes using Cursor Composer:
   - Update functionality
   - Maintain consistency
   - Ensure backward compatibility
   - Update documentation
Example format: "@[relevant file] Make it so that [specific change requested]"
```
--------------------------------------------------------------------------------
# Process-Specific Development Prompts

## Initial Project Setup Prompt
```markdown
Please help set up a [project type] with the following modern stack:
- Frontend: Next.js [version]
- UI Components: shadcn/ui
- Styling: Tailwind CSS
- State Management: Zustand
- Database: [specification]
- ORM: Prisma

Required clarifications:
1. Single user or multi-user?
2. Local or cloud database?
3. Additional feature requirements?
4. Performance constraints?

Please provide a detailed plan covering:
- Project structure and configuration
- Dependency setup with versions
- Component architecture
- State management approach
- Database schema design
```

## Infrastructure Implementation Prompt
```markdown
Based on the approved plan, please implement the core infrastructure:

1. Project Scaffolding
   - Next.js installation with app router
   - Tailwind CSS configuration
   - PostCSS setup
   - shadcn/ui integration
   - Prisma initialization

2. Configuration Requirements
   - Environment variables
   - Database connection
   - Build settings
   - Development tools

Please ensure proper error handling for:
- Dependency conflicts
- Build process issues
- Configuration errors
- Database connection problems
```

## Feature Implementation Prompt
```markdown
Please implement [feature] with the following structure:

1. Components Required
   - UI components (shadcn/ui)
   - State management (Zustand)
   - API routes
   - Database operations

2. Implementation Details
   - Component hierarchy
   - State structure
   - API endpoints
   - Error handling
   - Styling approach

3. Integration Points
   - State connections
   - API interactions
   - Database operations
   - UI updates
```

## Error Resolution Prompt
```markdown
Error encountered during [operation]:

1. Current Status
   - Error message: [details]
   - Recent changes: [list]
   - Environment: [details]
   - Dependencies: [versions]

2. Required Information
   - Build logs
   - Configuration files
   - Related components
   - Recent changes

Please provide:
1. Root cause analysis
2. Immediate fix steps
3. Prevention measures
4. Documentation updates
```

## Component Integration Prompt
```markdown
Please help integrate [component] with these requirements:

1. Technical Requirements
   - State management integration
   - API connections
   - Error handling
   - Styling requirements

2. User Interface
   - Component layout
   - Interaction patterns
   - State feedback
   - Error states

3. Data Flow
   - State updates
   - API calls
   - Error handling
   - Loading states
```

## Optimization Request
```markdown
Please optimize [component/feature] considering:

1. Performance Metrics
   - Load time
   - Response time
   - Resource usage
   - State updates

2. Code Quality
   - Component structure
   - State management
   - Error handling
   - Documentation

3. User Experience
   - Interaction feedback
   - Error messages
   - Loading states
   - Visual consistency
```
--------------------------------------------------------------------------------
# Process-Specific Prompts for AI Coding Assistant

## Project Initialization

```markdown
Please guide me through terminal-based project initialization for [framework]:

Project details:
- Name: [name]
- Framework: [framework]
- Technical stack: [technologies]

Please provide:
1. Exact terminal commands
2. Configuration options
3. Dependency verification steps
```

## Deep Seek Requirements Generation

```markdown
I'm developing [project type]. Please create a detailed requirements document covering:

1. Project overview
2. Core features
3. Technical requirements
4. Implementation guidelines

Use Deep Seek R1 model and search functionality to validate technical approaches.
```

## Cursor Rules File Creation

```markdown
Please help create a .cursor.rules file for my [framework] project:

Project context:
- Framework: [framework]
- Technical stack: [stack]
- Development focus: [focus]

Based on cursor.directory templates, include:
1. AI agent characteristics
2. Technical proficiency
3. Development guidelines
```

## Documentation Integration

```markdown
Please help integrate documentation for:
[List of frameworks/libraries]

For each source:
1. Access Settings > Features
2. Add documentation URL
3. Verify integration
4. Confirm version compatibility
```

## Design Implementation with Deep Seek

```markdown
Please analyze this design screenshot and create:

1. Detailed UI specifications
2. Color palette
3. Typography guide
4. Component structure
5. Implementation guidelines

Use Deep Seek to generate comprehensive design documentation.
```

## Feature Development

```markdown
Please implement [feature] following these guidelines:

1. Review requirements.md
2. Start with basic implementation
3. Add complexity incrementally
4. Maintain project standards

Context:
- Current state: [description]
- Requirements: [reference]
- Technical constraints: [list]
```

## Documentation Update

```markdown
Please update project documentation for:
[Feature/Component]

Update:
1. requirements.md
2. Technical documentation
3. Implementation guidelines
4. Configuration details

Ensure alignment with Deep Seek generated requirements.
```

## Design Translation

```markdown
Please convert this design screenshot into implementable code:

Design elements:
- Layout structure
- Color scheme
- Typography
- Components
- Interactions

Follow Deep Seek generated specifications for accuracy.
```
--------------------------------------------------------------------------------

*Code Generation Protocol*
```markdown
"Develop a [language] solution for [specific requirement] considering:
- Primary use case: [describe]
- Edge cases: [list]
- Performance constraints: [specify]

Present:
1. Architecture options table comparing OOP/functional/reactive approaches
2. Memory/performance characteristics for each
3. Recommended implementation with failure points highlighted"
```

*Debugging Workflow*
```markdown
"Analyze this [language] error:
[Paste error/logs]

Follow diagnostic protocol:
1. Isolate failure context (≤5 lines)
2. Create causality chain diagram
3. Suggest 3 mitigation strategies with hot-patching viability assessment"
```

*Code Review Template*
```markdown
"Conduct comprehensive review of this [language] module:
[Paste code]

Evaluate:
- SOLID compliance level (0-100%)
- Cyclomatic complexity score
- Test coverage requirements
- Alternative pattern suggestions

Format findings as:
✅ Strengths | 🚫 Concerns | 💡 Optimization Opportunities"
```

--------------------------------------------------------------------------------

*   **Prompt 1: Code Explanation**
    ```
    "I am currently looking at the following code: [paste code snippet]. Can you explain what this code does, focusing on [specific aspect, e.g., the purpose of the `copy` variable or how does strick mode works], and any potential implications of this code?"
    ```

*   **Prompt 2: Multiple File Understanding**
    ```
   "I have the following files in my project: [list of file names like index.js and readme]. In the context of these files, can you explain the output of 'output what is said in the read me and what is the header text' and how are these files interconnected when doing this kind of prompt?"
    ```
*  **Prompt 3: Code Generation**
    ```
    "I want to add [specific functionality] to my app, such as ['Center hello world could we also add a button under it in column format saying that was easy that was easy make it a around rectangle when I click it shows a text saying subscribe' or 'add a s scroller game with a high score make all the designs in bit' ] in index.js, using react. Can you provide the code for this, focusing on [specific UI elements, functionality, or structure, if any]?"
    ```

*  **Prompt 4: Deployment Guidance**
    ```
    "I am trying to run my react application and it's giving errors. I have the package.json file. I am also using an external terminal. Give me step-by-step instructions on how to access the correct directory and launch LocalHost 3000"
   ```

*   **Prompt 5: Github Guidance**
    ```
    "I need help to connect my local files to github. I am using a private repository and I'm using access token. Provide me step-by-step instructions on all the commands that are required to push a current git branch."
    ```
--------------------------------------------------------------------------------

*   **Initial Project Setup (Cursor):**

    ```
    Create a new web application with a React front end. Use the create-react-app command and install necessary packages (e.g., react-youtube, react-router-dom, shadcn/ui).
    Provide me a folder structure for the setup with specific files and folders and place the files correctly within the directory.
    ```

*   **Feature Implementation (XML Tagged Prompt):**

    ```xml
        <description>
            I want to create a [feature description, e.g., image generator]. This feature should [detail the expected behavior, e.g., take a prompt and return a image url].
        </description>
        <requirements>
            [List specific requirements and dependencies, e.g., integrate with the replicate API, add image url to the CSS, make it a dark theme, use structured output for data validation and type safety, provide a loading status and error message if there are issues].
        </requirements>
        <action>
            Create all the needed code to implement this into the project, using the provided description and requirements.
        </action>
        <folderStructure>
          Provide the structure where the files need to be placed.
        </folderStructure>
    ```

    *(Example:*

    ```xml
        <description>
             I want to add stripe payments to my react app. The payments must be on hold until I as the admin confirm the payment.
         </description>
         <requirements>
              Integrate with firebase functions to send people to stripe check out. Use the stripe extension on firebase. Set the capture method to manual. Create an admin interface. Use structured outputs for data validation. Provide a loading status and error message for API calls.
         </requirements>
         <action>
              Create all the needed code to implement this into the project, using the provided description and requirements.
         </action>
         <folderStructure>
           Provide the structure where the files need to be placed.
         </folderStructure>
    ```

    )*
*   **UI Styling & Layout (Image Prompt):**

    ```
     <image> [upload your image] </image>
     Based on the design of my uploaded image update the styles of my web application to look exactly the same.
    Also align the components vertically and horizontally as described in the image.
    Keep a minimalistic design, use dark theme with high contrast and good readability.
    ```
*   **Component Modification (Chat):**

    ```
    Modify the [component name, e.g. Subpage.js ] component to [describe the specific change, e.g. add a new text field, center buttons]. Use the code base as context. Also try to optimize the component for performance.
    ```
*   **Code Debugging:**

    ```
    I am getting the following error in the code [paste error here]. Can you help me resolve it please? Use the full code base as context.
    ```
*   **Back-end Integration (Firebase Functions):**

    ```
    I'm ready to deploy this application on Firebase. Create functions that will handle [describe what the functions should do, e.g., initiate stripe checkouts, confirm payments]. Also set up the stripe extension on Firebase. Provide error handling and user feedback.
    ```
*  **Data Fetching Prompt:**

    ```
       Fetch the data from this API endpoint [API endpoint]. Display the data in a table or a card component. Provide loading states and error handling.
    ```
*   **Image Manipulation Prompt:**

    ```
       I want to add image manipulation to my web application using [API like replicate]. Create an image input field and create different sliders to modify the image. Optimize the performance for the component and make it easy to use.
    ```
*   **Generate Documentation:**

    ```
      Based on the code in my project create a a simple description for each tool, generate SEO friendly metatags, generate a robots.txt file and generate sitemap.xml.
    ```
*   **Cursor Rules Configuration:**

    ```
       Based on the Open AI API for structured output, write a cursor rule that instructs the AI to always use structured output using pydantic.
    ```
*   **File Manipulation:**

    ```
          Create a file named [filename] and include this code in this specific file. Also create all the folder necessary to create this file in the correct place.
    ```
*   **Large File Generation:**

    ```
       Create the following folder and file structure including basic placeholder code in every file.
      [paste in folder structure here]
    ```
*   **Combine Different Models or AI Tools:**

    ```
        Combine different tools for this task. For code generation use [Model] and for debugging use [Model2]. For image generation use [Image API].
    ```
*   **Generate Placeholder:**

    ```
    Create the following placeholder text and components for my web page.
    [Description]
    ```
*   **Convert Component using AI:**

    ```
        I want to convert the following component [component name], to a component that [description of desired conversion].
    ```
 * **User Feedback and Error Handling:**
    ```
      Create an error handling for this specific function or process, provide feedback to the user using a loading message and error state to see if there are any issues with the asynchronous operations.
    ```
*  **Performance Optimization Prompt:**
    ```
         Optimize this specific component for performance, including things like lazy loading, or defer rendering of non crucial elements in the UI.
    ```
--------------------------------------------------------------------------------
# Process-Specific Development Prompts

## Project Initialization

```xml
<initializationPrompt>
    <requirements>
        - Next.js application
        - TypeScript support
        - Shadcn/UI components
        - Firebase backend
    </requirements>

    <commands>
        Generate required setup commands
        Create directory structure
        Initialize configuration files
        Setup environment variables
    </commands>
</initializationPrompt>
```

## Component Development

```xml
<componentPrompt>
    <visualContext>
        [Design screenshot/mockup]
        [Layout specifications]
        [Interaction patterns]
    </visualContext>

    <requirements>
        - Component functionality
        - Styling requirements
        - Integration points
        - State management
    </requirements>

    <implementation>
        - Generate component code
        - Setup styling
        - Add functionality
        - Implement integration
    </implementation>
</componentPrompt>
```

## Firebase Integration

```xml
<firebasePrompt>
    <setupRequirements>
        - Pay-as-you-go plan
        - Firebase project creation
        - Environment configuration
        - Deployment setup
    </setupRequirements>

    <configuration>
        - Firebase config object
        - Environment variables
        - Security rules
        - Hosting setup
    </configuration>

    <deployment>
        - Build commands
        - Deploy procedure
        - Domain setup
        - Verification steps
    </deployment>
</firebasePrompt>
```

## Stripe Integration

```xml
<stripePrompt>
    <setup>
        - API key configuration
        - Test/Live mode setup
        - Webhook configuration
        - Error handling
    </setup>

    <implementation>
        - Payment flow
        - Success/Error handling
        - Webhook processing
        - Testing procedures
    </implementation>
</stripePrompt>
```

## SEO Implementation

```xml
<seoPrompt>
    <requirements>
        - Meta tags setup
        - Sitemap generation
        - Robots.txt configuration
        - Schema markup
    </requirements>

    <implementation>
        - Generate required files
        - Configure meta data
        - Setup dynamic routes
        - Implement schemas
    </implementation>
</seoPrompt>
```

## Error Resolution

```xml
<errorPrompt>
    <context>
        [Error message]
        [Stack trace]
        [Environment details]
    </context>

    <resolution>
        - Error analysis
        - Solution implementation
        - Testing procedure
        - Prevention measures
    </resolution>
</errorPrompt>
```

## Performance Optimization

```xml
<optimizationPrompt>
    <targets>
        - Loading performance
        - Runtime performance
        - Build optimization
        - Asset optimization
    </targets>

    <implementation>
        - Identify bottlenecks
        - Implement solutions
        - Measure improvements
        - Document changes
    </implementation>
</optimizationPrompt>
```
--------------------------------------------------------------------------------
## Code Generation

### Basic Code Generation
*   "Create a `[type of application/game]` using `[language/framework]`."
*  "Generate a `[type of content]` with `[specific features/details]`"
*  "Please create a `[type of application]` using `[specific libraries or frameworks]`"
* "Please create a `[type of application]` that should include the following functionality `[list of required functionality]`"
*  "Please have a look at `[documentation file]` to get an initial understanding of the application, create an implementation plan that combines the findings from your analysis. Use chain of thought reasoning to create a plan so we can write modularized and optimized code."
*  "Please have a look at `[implementation file]` and start with implementing the first phase `[name of the first phase]`. Now the document will say that we've already implemented `[name of the component/feature]`, this is not correct. You can find a boilerplate for this project in `[state management file]`. However, if you think we should add anything or we do too much in the `[name of the component/feature]` definition, please explain before you start writing the code. If you think this is correct and actually a good starting point, you can just start to write the code and walk me through it step-by-step so that I can test the feature from Phase I. Keep in mind, the ui has to look like `[image file]`"
*   "I want you to create a `[type of application]` by looking at the `[source folder]`"

### Code Modification
*  "The implementation is not correct because of the following reasons `[reasons for not being correct]`, please fix the issues in the code"
*  "I've noticed that I don't have the following `[component/feature]`, please add this to the implementation."

## Debugging and Error Resolution

*   "I've tried to run the application and I get the following error `[error description]`, could you please use Chain of Thought reasoning to explain where the error comes from exactly and then propose a plan to fix it and walk me through it step by step."
*  "I get the following error `[error description]`, so could you please go ahead and fix it and walk me through it step by step."
*  "The implementation is working, but I would like to proceed with the next steps according to `[implementation file]`."
*  "The implementation matches all the requirements in the workflow description so no additional changes are needed. Okay, so could you then please go ahead and explain why I don't see the implementation working as expected and explain the following error `[error description]`. Please use Chain of Thought reasoning and fix the error and walk me through it step by step."
*  "The `[component/feature]` is not behaving as expected, please fix all of the issues. First, please tell me where they occur and then fix them, walk me through it step by step."

## Project Planning
*   "I want to create a `[type of application]` with `[languages/frameworks]`. Please play the role of an experienced senior dev and project planner. I have absolutely no idea how to tackle such a project. I need you to ask clarifying questions and then reverse engineer what libraries, tools, providers, features, database schemas / tables I would need to successfully create such an application. Leave nothing out and talk about all of the necessary moving parts of such a fullstack application. Basically, I need you to plan the whole process for me as specific as possible with a clear step by step plan and todos to follow so that I can give the plan to a developer and let him create the app."

## General Chat Instructions
* "Let me know if I can help you with anything else"
*  "Please proceed"

## Additional Prompt Structure Information
*   **File Context:** The prompt should use a specific tag to reference files or folders and specify the type, for example: `[# file: document.md]` or `[# folder: src]`.
*   **Chain-of-Thought:** The user explicitly requests "Chain of Thought" reasoning in certain prompts. This guides the AI to explain its thought process before providing a solution.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
# END