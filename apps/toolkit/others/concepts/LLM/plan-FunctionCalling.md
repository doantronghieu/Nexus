# Request Processing Flow

## 1. Query Analysis and Function Mapping
- LLM processes user query and function descriptions
- Determines function requirements and parameter mapping
- Returns structured function execution plan:
  ```json
  [
    {
      "name": "FUNCTION_NAME_1",
      "params": {
        "PARAM_1": VALUE,
        "PARAM_2": VALUE
      },
      "priority": 1
    },
    // Additional functions...
  ]
  ```

## 2. Function Execution and Response Generation
### If Functions Are Required
- System extracts function parameters
- Executes functions based on priority:
  - Priority 1 functions execute first
  - Same-priority functions execute in parallel for optimization
- Awaits function results
- LLM evaluates results against user query:
  - If satisfactory: Generates response using original query + results
  - If unsatisfactory: Repeats step 1 with execution history

### If No Functions Required
- LLM processes original query directly

## System Requirements
- Supports concurrent function execution
- Manages parallel processing for same-priority functions
- Aggregates all function results before final LLM response
- Ensures natural language response generation

---

Implement system prompt for LLMTitan