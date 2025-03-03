### Introduction
- **Critique of the Name "Function Calling"**:
  - The name "function calling" is criticized as inaccurate.
  - The feature is about controlling the format of the model's output, not the model calling functions.

### OpenAI's Function Calling
- **OpenAI's Process**:
  - The feature requires informing OpenAI about the functions' schema.
  - The user parses the model's output into JSON and calls the function.
  - OpenAI does not call the function; the user's program does.
  - Step-by-step process involves:
    - Informing OpenAI about the functions.
    - Using the chat API to ask the model a question.
    - Parsing the model's output string into JSON.
    - Extracting values and calling the function.

### Ollama's Format JSON
- **Ollama's Process**:
  - Ollama refers to this feature as "format json," which is more descriptive.
  - It can be used via API or CLI.
  - Requirements:
    - Define a payload with a model and an array of messages.
    - No need for a system prompt as it is already included in the model.
  - Example in Python:
    - Importing requests.
    - Defining a payload with the model and messages.
    - Sending a POST request to the chat endpoint.
    - Printing the JSON response.
    - Iterating through the response for streaming.

### Implementation in Python
- **Dynamic Script**:
  - The script can be made dynamic by taking command-line arguments.
  - Example:
    - Importing sys and setting the country variable from command-line arguments.
    - Changing the content in the payload to include the country.
    - Example command: `python fc.py France` returns Paris.

### Additional Features
- **Calculating Distances**:
  - The script can be extended to calculate distances using the Haversine package.
  - Example:
    - Changing the question to ask for the decimal latitude and longitude of the capital.
    - Adding a system prompt to request JSON output.
    - Adding "format json" to the payload for better consistency.
    - Providing a schema to the model.

### Schema and Consistency
- **Schema and Few-Shot Prompt**:
  - Providing a schema to the model to ensure consistent key names.
  - Using a few-shot prompt if the model's response is not consistent with the schema.
  - Example:
    - Disabling streaming for JSON responses.
    - Setting cityinfo to the JSON string in the message content.
    - Calling the Haversine function with the coordinates.

### Comparison and Opinion
- **Comparison**:
  - The speaker prefers Ollama's native API over OpenAI's more complicated approach.
  - The speaker questions the value of the OpenAI approach just for the brand name.

### Call to Action
- **Engagement**:
  - The speaker asks viewers for their thoughts on the feature and if they are using it.
  - Viewers are encouraged to suggest other features they'd like to see in the comments.
  - The speaker expresses gratitude for the community's input and ideas for future videos.

### Conclusion
- **Closing Remarks**:
  - The speaker thanks the viewers for watching and encourages them to keep the comments coming.

---

### Introduction
- **Topic**: OpenAI Function Calling
- **Purpose**: Discuss how OpenAI Function Calling works

### Key Points
1. **Function Calling Overview**:
   - OpenAI does not call functions itself.
   - It suggests which function to call and with which parameters.
   - This functionality helps to pull in external data into LLM applications and prompts.

2. **Components**:
   - Functions
   - Application
   - OpenAI API
   - LLM (e.g., GPT 3.5, GPT 4)

3. **Process**:
   - Application creates function definitions and a prompt.
   - API converts this into a system prompt containing functions and the original prompt.
   - LLM processes the system prompt and suggests function names and parameters.
   - Application calls the suggested function with the provided parameters.
   - Results are sent back to the API and then to the LLM for final processing.

4. **Code Example**:
   - Weather example using OpenWeatherMap API.
   - Functions defined include `get_current_weather` with latitude and longitude parameters.
   - Application makes API calls, processes responses, and updates the message history.

5. **Multiple Function Calls**:
   - The system can handle multiple function calls in a single prompt.
   - Example: Getting weather for Paris and San Francisco simultaneously.

6. **Additional Notes**:
   - Function calling is optional; the functionality can also be used to extract structured data.
   - Similar functionality may be available with other models like Mistral's closed-source models.

7. **Further Learning**:
   - A video is suggested for learning how to extract structured data without function calling.

### Detailed Steps in the Code Example
1. **Imports and Initialization**:
   - Import necessary libraries.
   - Initialize the OpenAI client.

2. **Function Definition**:
   - Define `get_current_weather` function that takes latitude and longitude.
   - Make a call to the OpenWeatherMap API using the provided parameters.
   - Process the response and return the weather data.

3. **Run Conversation**:
   - Create a prompt and add it to a messages array.
   - Define tools (functions) with type, name, and parameters in JSON schema format.
   - Make a call to the OpenAI API with the messages and tools.
   - Process the response to extract tool calls.
   - Check for tool calls and update the messages array.
   - Define a dictionary to map function names to actual functions.
   - Iterate over tool calls, find the corresponding function, and call it with the provided arguments.
   - Add the function call results to the messages array.
   - Make a second call to the OpenAI API with the updated messages array.

4. **Example Prompt**:
   - Ask for the weather in Paris.
   - Call the `run_conversation` function with the prompt.
   - Print the responses from the API and LLM.

5. **Multiple Locations**:
   - Update the prompt to ask for the weather in Paris and San Francisco.
   - Call the `run_conversation` function again.
   - Observe the responses for both locations.

### Conclusion
- OpenAI Function Calling is a powerful tool for integrating external data into LLM applications.
- It can handle multiple function calls in a single prompt.
- Function calling is optional and can also be used to extract structured data.

---

### Introduction
- The video is about function calling in LLMs (Large Language Models).
- The speaker aims to explain function calling in the simplest way possible.

### Example
- Example prompt: "What is the current Apple stock price?"
- A model executes a Python function to retrieve the stock price.
- The LLM then provides a response with real-time data.

### Video Structure
- The video is divided into two main sections:
  - Explanation of what function calling is and how it works.
  - Implementation steps.

### Benefits of Function Calling
- Function calling helps LLMs carry out specific tasks reliably.
- It provides flexibility and customization, allowing LLMs to behave in a certain way.
- It helps with inconsistent answers, real-time data retrieval, and executing actions without using agents.

### Examples of Function Calling
- ChatGPT's premium feature allows searching the internet for answers.
- Function calling can connect LLMs to various applications like CSV files or other functions.

### Implementation Tutorial
- The tutorial is broken down into four main sections:
  - Defining the function.
  - Simple function calling with a basic prompt.
  - Advanced function calling using the OpenAI package.
  - Extending the function further using OpenAI.

### Defining the Function
- Install necessary packages (e.g., yfinance for stock prices).
- Define a function to retrieve stock prices using Yahoo Finance.
- Example: Retrieve the stock price for Apple.

### Simple Function Calling
- Convert the function into a string.
- Use a prompt to get the stock code and format it for the function.
- Send the prompt to the chat model.
- Instantiate the OpenAI model and get the API key.
- Parse the response to execute the function.

### Advanced Function Calling
- Import the OpenAI client.
- Define the function and messages.
- Use tools (metadata of the function) to define the function's functionality.
- Get the response from the model and print the tool call.
- Execute the function and get a more tailored answer.

### Extended Function Calling
- Use the initial response to pass it onto the model with various functions.
- Get a more refined and accurate answer.
- Example: Retrieve stock prices for Nvidia and Alibaba.

### Additional Information
- Mention of Mistral for open-source LLMs.
- Link provided for Mistral AI implementation of function calling.

### Conclusion
- The main concept is to use a user function to call the API, which returns information that is then passed back to the model for a more tailored and accurate response.
- The video encourages viewers to subscribe for similar content.

---

