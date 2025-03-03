# Beginner's Guide to AI-Assisted Development

## Understanding Your Tools

### Cursor IDE Features
1. Cursor Composer
   - Implements code changes directly
   - Requires [code base] tag
   - Can work with screenshots
   - Modifies existing code

2. Chat Option
   - Provides explanations and solutions
   - Doesn't implement changes
   - Good for learning concepts
   - Helps understand errors

### V.D Design Tool
- Creates front-end designs
- Provides design references
- Can be used with Cursor Composer
- Helps visualize your app

## Getting Started

### 1. Project Setup
```bash
# Create a new project
npx create-expo-app your-app-name

# Go to your project folder
cd your-app-name
```

### 2. Setting Up Cursor
1. Open Cursor IDE
2. Create .cursor.rules file
3. Add documentation:
   - Expo docs
   - React Native guides

### 3. Using Cursor Composer
Always remember:
1. Use [code base] tag for implementations
2. Take screenshots for visual references
3. Show errors with screenshots
4. Be specific about changes needed

## Development Workflow

### 1. Design Phase
1. Use V.D:
   - Specify app type
   - List design requirements
   - Get design preview
2. Take screenshot of design
3. Use with Cursor Composer

### 2. Implementation Phase
1. Present design to Cursor Composer:
   ```
   I want my screen to look like this:
   [Screenshot]
   [code base]
   ```

2. Review and refine:
   ```
   Please change [specific element]:
   [Screenshot]
   [code base]
   ```

### 3. Testing
1. Web testing:
   ```bash
   npm run web
   ```

2. Device testing:
   - Install Expo Go app
   - Scan QR code
   - Test on your phone

### 4. Error Handling
1. Take screenshot of error
2. Show to Cursor Composer:
   ```
   I'm seeing this error:
   [Error screenshot]
   [code base]
   ```

## Best Practices

### 1. Clear Communication
- Be specific about requirements
- Use screenshots for visual references
- Explain what you want to change
- Show before/after states

### 2. Proper Tagging
- Always use [code base] for implementations
- Use without tags for explanations
- Include [RQ] for requirements
- Be consistent with tagging

### 3. Testing
- Test on web browser first
- Use Expo Go for device testing
- Test on both Android and iOS
- Verify all features work

### 4. Design Integration
- Start with V.D designs
- Take clear screenshots
- Show full screen views
- Point out specific areas for change
--------------------------------------------------------------------------------
# Practical Guide

## Best Practices:

*   **Start with a Clear Idea:** Focus on solving a specific user pain point with a simple, shareable solution.
*   **Leverage Existing Designs:** Don't reinvent the wheel; use Mobbin to find proven app flows.
*   **Plan Thoroughly:** Create a detailed context file to guide Cursor AI's code generation process. This includes the database schema and folder structure.
*   **Iterate and Test:** Develop the app incrementally, testing each component along the way.
*   **Prioritize User Experience:** Copy UI elements from high quality apps through mobin.
*   **Use specific development commands**: When running your expo project, be sure to run 'npx expo start' to initialize it, when reloading the app after modifications be sure to press R in the terminal.

## Workflow:

1.  **Ideation:** Find a problem, simplify the solution and make it shareable.
2.  **Design:** Use Mobbin to copy design flows into Figma.
3.  **Structuring:** Create a context file to provide a detailed plan of the app's behavior.
4.  **Code Generation:** Use Cursor AI to build the app step-by-step, referring to your context file.
5.  **Backend:** Integrate Superbase for data storage and user authentication.
6.  **AI:** Add the DeepSeek AI chat feature.
7.  **Deployment:** Upload your Expo app to the App Store and Play Store.

## Implementation Tips:

*   **Use Markdown:** Format your context file using markdown for better readability.
*   **Tag Files:** When using Cursor AI, tag your context file (e.g., `@context.md`) to ensure the AI refers to your project information.
*   **Copy and Paste:** Copy error messages and use them as prompts to debug problems in cursor ai.
*   **Environment Variables:** Use an `.env` file to store sensitive information like API keys and tokens.
*   **Step by Step Development**: When generating code, focus on one task at a time. Break down large tasks into smaller, more manageable parts.
*   **Troubleshooting**: If the app does not work as expected, use the cursor ai chat to give context and get solutions.
--------------------------------------------------------------------------------
# Generic Practical Guide: Mobile App Development

This guide offers best practices, general workflows, and useful tips for building mobile applications.

## Best Practices

*   **Start with Core Functionality:** Focus on implementing core features first before moving to more advanced ones.
*   **Use Official Documentation:** Always refer to the official documentation for each technology you are using.
*   **Incremental Testing:** Test regularly and frequently during each phase of development.
*   **Utilize Version Control:** Use Git or similar version control tools for tracking changes and collaboration.
*   **Well-defined Requirements:** Ensure that you have clear and well-defined requirements before starting.
*   **Modular Code:** Write modular and reusable code.
*   **AI Assistance:** Use AI code editors to help write code but always review and understand it.
*  **Documentation Tagging:** Tag the documentation inside your code editor to keep your AI assistant updated with the latest information.

## Workflow

1.  **Project Setup:**
    *   Initialize a React Native project using Expo.
2.  **UI Development:**
    *   Design the basic layout of your application's user interface.
    *   Style the UI using a suitable styling solution.
3.  **Feature Implementation:**
    *   Integrate features one at a time, and test them after implementing each one.
4.  **Backend Integration:**
    *   Set up a backend service and create the necessary database (if required).
    *   Establish an API connection for data transfer.
    *   Use an environment file to store all API keys.
5.  **AI Integration:**
    *  Integrate AI functionality, as needed.
    *  Store API keys safely using environment variables.
6.  **Testing and Debugging:**
    *   Test the application on target platforms (iOS, Android, Web).
    *   Use debugging tools to troubleshoot errors.

## Implementation Tips

*   **Code Editors:**
    *   Utilize AI code editors for code generation and auto-completion.
    *   Take advantage of AI assistant features for easier code understanding.
    *  Tag your technology documentation inside your code editor.
*   **Expo:**
    *   Use Expo for a faster development cycle.
    *   Leverage Expo tools for testing on mobile platforms.
*   **Backend Services:**
    *   Utilize serverless or backend-as-a-service platforms as needed.
    *  Make sure to store API keys securely using environment files.
*   **AI Integration:**
    *   Select AI services that align with your application goals.
    *   Store API keys and related credentials securely.
    *   Consult the documentation for the chosen AI service.

## Additional Notes
* This practical guide assumes you will tag the documentations for your technologies inside your code editor.
* This practical guide is designed to be generic and can be applied to different application types. For further details, please refer to official documentation for each technology.
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
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
# END