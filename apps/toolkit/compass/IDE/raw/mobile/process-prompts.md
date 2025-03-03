# Process-Specific Development Prompts

## Initial Project Setup
```
I want to create a [type] app using React Native and Expo. I am a beginner.

[RQ] Requirements:
1. [List basic requirements]
2. [List core features]

[code base]
```

## Design Implementation with V.D
```
Please create a front-end design for my [type] app.

Requirements:
1. [List design requirements]
2. [List specific features needed]

[Attach V.D generated design]

[code base]
```

## Design Implementation with Cursor Composer
```
I want my screen to look exactly like the attached screenshot.

[Attach screenshot]

Please implement this design.

[code base]
```

## Error Resolution
```
I am seeing these errors in my app:
[Attach error screenshot]

Please help fix these errors.

[code base]
```

## Design Refinement
```
This is how my app looks right now:
[Attach current screenshot]

I don't like [specific aspect]. Please improve it.

[code base]
```

## Testing Setup
```
I want to test my app on [platform].
Current implementation:
[Describe/show current state]

[code base]
```

## Documentation Request
```
I need help understanding:
1. [Specific feature/concept]
2. [Technical term]

Please explain in simple terms.
```

Note: Always use the [code base] tag when requesting implementations or changes through Cursor Composer. Use without the tag for explanations through chat.
--------------------------------------------------------------------------------
*   **App Ideation:**

```
"Based on the following principles: identify a common problem, keep the core functionality simple (three words or less), and make the solution easily shareable, suggest three potential app ideas. After listing each idea, ask if I'd like to explore it further.  If I choose to explore it, ask if there is anything specific I would like to focus on within this idea.  If I don't, move onto the next idea."
```

*   **Design Replication:**

```
"Using Mobbin, find a design that closely matches my app concept. Provide a rationale for why you think this design is suitable. Then guide me through the process of extracting the design flow into Figma, and finally cleaning up my Figma file. Please provide clear instructions on how to import these designs into Figma for use with Cursor AI."
```

*   **App Structuring:**

```
"Now, help me structure the 'brain' of my app. Please guide me in creating a detailed context file, using the user defined needs and desired app functionality. Include clear explanations on how to organize my ideas for use by Cursor AI. Additionally, please give the proper prompt to create a database schema, optimal folder structure, and add it to the context file."
```

*  **Code Generation with Cursor AI:**

```
"I have created my context file (context.md) which provides the context to develop my app. Based on that context file, and the defined structure of the app, please generate a development plan. Then, provide the specific steps required to implement it. Provide step-by-step instructions, and be prepared to generate the code. Be sure to include instructions and commands on installing any libraries or other files necessary for the code to work. When providing code, make sure it is correctly formatted and easy to copy and paste into my development environment. Please pay attention to the specific needs of the project using my context.md file as a reference"
```

*   **Backend Integration (Superbase):**

```
"Guide me through the process of setting up Superbase for my app's database and authentication. This includes creating a new Superbase project, obtaining the necessary API keys and URLs, and integrating them into my app. Then generate the code to implement login and signup flows using the superbase authentication library."
```

*   **AI Feature Integration (DeepSeek API):**

```
"Guide me through the process of setting up the DeepSeek API for my app's AI chat feature. This includes obtaining the DeepSeek API key and integrating the chat feature into my app. After integration, prompt me to test the function of the AI chat in my app. When giving code snippets for the integration, be sure to include any necessary import statements."
```

*   **Deployment (App Store/Play Store):**

```
"Guide me through the steps required to upload my Expo app to both the App Store and Google Play Store, including necessary steps like creating accounts on Expo, Apple developer program and Google Play developer program. After that give step by step instructions of the necessary steps to prepare and upload my app."
```
--------------------------------------------------------------------------------
``markdown
# Generic Process-Specific Prompts for AI Coding Assistant

These prompts are designed to guide the user through common mobile development tasks.

## 1. Project Setup

**Prompt:**
"I'm starting a new mobile app project. Please provide instructions for setting up a new React Native project using Expo, including all necessary commands and explanations. "

**Expected Assistant Behavior:**
* Provide the command to create a new Expo project
* Explain that the user needs to pick a project name.
* Explain that they need to go into the project directory after the project has been created
* Provide the npm start command to begin testing
* Explain the QR code and Expo GO mobile app scanning process.

## 2. Basic UI Development

**Prompt:**
"I have set up my project and want to start building the user interface. Provide guidance on how to structure a basic layout and style it using a styling solution."

**Expected Assistant Behavior:**
*   Guide user to create screen file
*   Provide sample react native code with basic view, Text and buttons components for home screen
*   Guide users on how to view the new screen
* Explain that any CSS or styling solution can be used.

## 3. Feature Integration

**Prompt:**
"I want to integrate a specific feature into my app. Please guide me on how to add \[feature name], including necessary code and dependencies. It should include any necessary permissions."

**Expected Assistant Behavior:**
*   Guide user to add a necessary components to start implementing feature
*   Provide the necessary library and its installation (if required)
*   Add the necessary code snippet with the permission handling (if required)
*   Explain that the user needs to add necessary permissions (if required)

## 4. Backend Service Integration

**Prompt:**
"I need to connect my application to a backend service. Guide me through the process of integrating \[backend service name], including database setup and API connections."

**Expected Assistant Behavior:**
*   Explain how to create a backend account or project.
*   Guide the user to find the necessary keys
*   Explain and guide user to install the package
*   Guide user on how to create an .env file and paste the keys
*   Explain how to set up database (if necessary)
*   Provide any required schemas and guide user on how to set them up.

## 5. AI Integration

**Prompt:**
"I want to add AI capabilities to my app. Provide instructions for integrating an AI service (like \[AI service name]), including API key setup and basic AI interactions."

**Expected Assistant Behavior:**
*   Explain how to create a AI API key or how to use a free key (if available)
*  Explain the process of using documentation for API integration
*   Guide the user to add the AI API documentation inside code editor.
*   Guide user to add AI API key inside environment variables
* Explain about any additional steps for AI integration

## 6. Debugging and Troubleshooting

**Prompt:**
"I'm encountering an error. Here is the error message: \[insert error message]. Please help me diagnose and resolve this problem."

**Expected Assistant Behavior:**
*   Ask the user where they are getting the error message from
*  Analyze the error message, provide probable causes and suggest solutions.
* Provide code changes, if needed.

**Note:** These prompts are now more generalized and can be used for a variety of applications.
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