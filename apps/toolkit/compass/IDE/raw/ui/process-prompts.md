# Process-Specific Development Prompts

## Project Setup Prompts

### Initial Setup
```
Please set up a new Next.js project with the following configuration:
- Next.js (latest)
- TypeScript
- Tailwind CSS
- Shadcn UI
Include the basic project structure and necessary configuration files.
Follow with git initialization and initial commit.
```

### Cursor Rules Setup
```
Create a cursor rules file with:
- Stack: react, nextjs, typescript, tailwind
- Emoji prefix: 🤖
- Essential rules only
Avoid overcrowding the context window.
```

### Shadcn Installation
```
Install Shadcn components with:
- Use 'npx shadcn/ui@latest init' (not shadcn-ui)
- Configure for proper installation
- Verify component availability
- Test component rendering
Monitor for and handle common installation issues.
```

## Component Development

### Design Implementation from Screenshot
```
Create a [component type] based on this design:
[paste design/screenshot]
Requirements:
- Match visual style
- Maintain responsive layout
- Use Shadcn components
- Follow existing color scheme
- Implement specified features
Monitor robot emoji for rules compliance.
```

### 21st.dev Component Integration
```
Integrate this component from 21st.dev:
[paste extended PR prompt]
Requirements:
- Adapt to current theme
- Maintain consistency
- Implement proper styling
- Add necessary animations
Verify proper integration and styling.
```

### Component Speed Adjustment
```
Modify the animation speed of [component]:
- Adjust speed parameters
- Maintain smooth animation
- Optimize performance
- Test across different scenarios
Implement custom speed controls if needed.
```

## Page Development

### Landing Page with Background
```
Create a landing page with:
- Animated background component
- Hero section with specific content
- Features section
- Call-to-action components
- Custom speed controls
Include theme customization options.
```

### Dashboard Implementation
```
Create a dashboard layout based on [screenshot/design]:
- Sidebar navigation
- Header components
- Chart implementations
- Widget sections
Follow the example structure and styling.
```

## Integration Workflows

### Design Resource Implementation
```
Convert this [Pinterest/Dribbble/other] design:
[design link/screenshot]
Into a functional component:
- Match visual style
- Ensure responsiveness
- Optimize performance
- Implement accessibility
Use git for version control and tracking changes.
```

### Component Library Integration
```
Integrate [component] from [library]:
1. Install dependencies
2. Copy component code
3. Adapt to project structure
4. Implement styling
5. Test functionality
Monitor for and resolve installation issues.
```

## Troubleshooting

### Shadcn Installation Issues
```
Resolve Shadcn installation problems:
1. Verify correct command usage
2. Check for conflicts
3. Install individual components
4. Test component rendering
Follow specific troubleshooting steps.
```

### Component Speed Optimization
```
Optimize [component] performance:
1. Analyze current implementation
2. Identify bottlenecks
3. Implement speed adjustments
4. Test and verify changes
Document successful optimization patterns.
```
--------------------------------------------------------------------------------
# Development Process-Specific Prompts

Structured prompts for different development phases, optimized for voice dictation and rapid development.

## Project Initialization

### Voice-Dictated Setup
```
I want to develop [project type] using [framework]. I'll be using [specific components] for the UI. The project needs [specific features]. Set up the environment for [operating system] and configure [development tools].
```

### Component Installation
```
Install [component library] using the latest version. For Shad CN, use:
npx shadcn-ui@latest init
Use [theme] for styling and set up [specific components].
Make sure to include proper TypeScript support.
```

### Dependency Management
```
Set up the project with:
- Framework: [specify version]
- UI components: [specify library and version]
- Additional tools: [list required packages]
Handle version conflicts and ensure compatibility.
```

## Project Structure

### Directory Organization
```
Create a project structure with:
- src/components for UI elements
- src/content for markdown files
- src/utils for utility functions
- pages/api for backend endpoints
Follow [framework] conventions for routing.
```

### Component Setup
```
Create [component name] using [library].
Include:
- Responsive design
- Error handling
- Loading states
- Integration with [other components]
```

## Terminal Operations

### Development Commands
```
How do I:
- Start development server
- Install dependencies
- Update packages
- Handle environment variables
```

### Error Resolution
```
For the error:
[Error message]
In [file/component]:
Analyze the issue and suggest fixes.
```

## Version Control

### Commit Management
```
Stage recent changes and:
- Generate descriptive commit message
- Include all modified files
- Document dependency updates
- Note any breaking changes
```
--------------------------------------------------------------------------------
# Process-Specific Prompts

## Initial Page Generation

```markdown
Create a marketing landing page for [company name] optimize it for high conversion
```

### Example Response Components
- Header with logo
- Hero section
- Features/Solutions section
- Testimonials
- FAQ section
- Contact form

## Design Iteration Commands

### Theme Changes
```markdown
Make it dark mode
Remove the light mode toggle
Make the logo white
Put a gradient on text titles (white to yellow)
Change the background from slate to neutral
```

### Layout Adjustments
```markdown
Make the three items appear in one row at medium page setting
Add an about us section with:
- Title and text on left
- Space for image on right
Change the email signup to a contact form
```

### Component Styling
```markdown
Put a circle around icons with a border
Make buttons completely rounded
Add a grid to the hero section background
Reduce title sizes by 20%
```

### Mobile Optimization
```markdown
Add a hamburger menu for mobile
Make menu stick to right side
Ensure proper mobile dropdown
```

## Deployment Preparation

```markdown
Set up the repository using:
npx create-next-app@latest [project-name]
cd [project-name]
[Add v0 command for importing components]
```

## Multi-Command Grouping

### Example Combined Commands
```markdown
"remove the light mode and have the dark mode as default
remove the toggle button
make the logo white
put a white yellow white to Yellow gradient on all the text titles"
```

## Design Forking
```markdown
Create a fork of the current design
Modify the new version with:
- Different color scheme
- Updated components
- Modified layout
While preserving the original
```
--------------------------------------------------------------------------------
# Process-Specific Prompting Templates

## V0 AI Prompting Templates

### Initial Component Creation
```
Please build a [component type] with a [style description] look.
Example: "Please build a notion-style landing page with a clean minimalistic look"
```

### Component Enhancement
```
Add [feature] to [component] with [specific behavior/animation].
Example: "Add a testimonial section with hover animation"
```

### Style Refinement
```
For the [component], please make it look more [style description] with [specific attributes].
Example: "For the testimonial card, please make them look more shadcn/ui-like, modern with that minimalistic feel but also feels like a premium startup"
```

### Layout Modification
```
Add [element] in the [location] [relative position reference].
Example: "Add an image in the hero section below the enter your email input and button"
```

## Claude AI Prompting Templates

### Code Organization Request
```
Please organize this code into separate components.
This is a [framework] application.
Please use [version] standards, not [deprecated approach].
Remember [specific requirement].
Please provide:
1. Complete file/folder structure diagram
2. Individual component breakdown
3. File organization with paths
4. All component code for copy/paste

Example:
"Please organize this code into separate components. This is a NextJS application. Please use NextJS 14 standards, not the pages router but app router. Remember app router and then give me the file/codebase structure and components to copy and paste."
```

### Structure Clarification
```
Forgot to mention [additional requirement].
Example: "Forgot to mention it's TypeScript buddy"
```

### Component Completion
```
[Action] the components.
Example: "Finish the components"
```

## Cursor AI Prompting Templates

### Bug Fix Request
```
[Component/element] looks [issue description].
Please fix.
Example: "The header looks weird and is not centered. Please fix."
```

### Visual Problem Resolution
```
Look at the [component]. This is how it looks: [screenshot/description].
Please fix it.
Example: "Look at the header navbar. This is how it looks [screenshot]. Please fix it."
```

### Feature Addition
```
Add [feature] to [component] with [specific requirements].
Example: "Add a dark mode toggle to the header with smooth transition animation"
```

## Integration Points

### V0 to Claude Transition
```
[Copy V0 output]
Please organize this code into separate components for [framework] using [version/requirements].
Provide file structure and individual components.
```

### Claude to Cursor Transition
```
[After implementing Claude's structure]
[Specific issue or feature request]
[Include visual context if needed]
```

## Response Handling

### Incomplete or Incorrect Responses
1. Clarify requirements
2. Provide additional context
3. Show visual examples if needed
4. Request specific modifications

### Iteration Requests
1. Build on previous output
2. Reference specific components/features
3. Maintain consistency with existing code
4. Preserve established patterns

Remember: Each tool has its strengths. Use the appropriate template for the specific phase of development you're in.
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
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------