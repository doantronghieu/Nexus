# Multi-Agent Calculator System Documentation

## 1. Overview
This document details the development of an expert system for arithmetic calculations using LangChain and LangGraph, featuring specialized agents for addition and multiplication operations.

### Key Features
- Specialized agents for mathematical operations
- Tool-based calculation execution
- Inter-agent collaboration through tool transfers
- Conversation history management
- Flexible routing mechanisms

## 2. System Architecture

### 2.1 Component Diagram
```
[User Input] → [Router] → [Addition Agent] ↔ [Multiplication Agent]
                   │           │                   │
                   └─[Tools]←─┴───[Calculation Tools]─┘
```

### 2.2 Core Components
1. **Agents**
   - Addition Expert (agent_add)
   - Multiplication Expert (agent_mul)
   
2. **Tools**
   - Calculation Tools: `add`, `multiply`
   - Transfer Tools: `tool_transfer_to_agent_add/mul`

3. **Message System**
   - Message state management
   - Tool call tracking
   - Result propagation

4. **Execution Graph**
   - LangGraph state management
   - Node transitions

## 3. Development Process

### 3.1 Initial Implementation
```python
class NODE(t.EnumCustom):
    AGENT_ADD = t.auto()
    AGENT_MUL = t.auto()

@tools_lc.tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@tools_lc.tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b
```

### 3.2 Key Challenges & Solutions

**Challenge 1: Tool Call Sequencing**
- **Problem**: Agents making single tool calls instead of required sequences
- **Solution**: Enhanced prompt engineering
```python
ADD_PROMPT = """You are an addition expert. For expressions like (a + b) * c:
1. Use add(a, b) 
2. Immediately transfer with tool_transfer_to_agent_mul"""
```

**Challenge 2: Message History Management**
- **Problem**: Lost conversation context during transfers
- **Solution**: Explicit message concatenation
```python
update={"messages": state["messages"] + [new_msg]}
```

**Challenge 3: Tool Response Handling**
- **Problem**: Missing tool_call_id mappings
- **Solution**: Comprehensive tool processing
```python
def process_tools(response, messages):
    for tool_call in response.tool_calls:
        tool_msg = ToolMessage(
            content=result,
            tool_call_id=tool_call["id"]
        )
```

### 3.3 Iterative Improvements

1. **Tool Registry System**
```python
TOOL_REGISTRY = {
    'add': add,
    'multiply': multiply
}

def register_tool(name: str, tool: BaseTool):
    TOOL_REGISTRY[name] = tool
```

2. **Enhanced Type Safety**
```python
class ToolFunction(Protocol):
    def invoke(self, tool_call: dict) -> Any: ...

ToolRegistry = Dict[str, ToolFunction]
```

3. **Unified Prompt System**
```python
SYSTEM_TEMPLATE = """You are {domain} expert. Rules:
1. {primary_task}
2. {collaboration_rules}"""

ADD_SPECIFIC = "Handle addition first, then transfer..."
```

## 4. Final Implementation

### 4.1 Agent Implementation
```python
def agent_addition(state: MessagesState) -> Command:
    model = create_tooled_llm(
        tools=[tool_transfer_to_agent_mul, add],
        system_prompt=SYSTEM_TEMPLATE.format(...)
    )
    # Process tools and manage state transitions
```

### 4.2 Tool Processing
```python
def process_tools(response: AIMessage, messages: list) -> tuple[list, bool]:
    for tool_call in response.tool_calls:
        if tool_call["name"] in TOOL_REGISTRY:
            tool = TOOL_REGISTRY[tool_call["name"]]
            result = tool.invoke(tool_call)
            # Handle result formatting
```

### 4.3 Graph Configuration
```python
builder = StateGraph(MessagesState)
builder.add_node(NODE.AGENT_ADD, agent_addition)
builder.add_node(NODE.AGENT_MUL, agent_multiplication)
builder.add_edge(START, NODE.AGENT_ADD)
graph = builder.compile()
```

## 5. Execution Flow

### 5.1 Successful Workflow
1. User input: "(3 + 5) * 12"
2. Addition agent:
   - Calculates 3+5=8
   - Transfers to multiplication
3. Multiplication agent:
   - Calculates 8*12=96
   - Returns final result

### 5.2 Error Handling
- **Tool Call Validation**: Ensure required tool calls
- **Message Integrity**: Full conversation history
- **Transfer Prevention**: Anti-looping mechanisms

## 6. Development Practices

### 6.1 Testing Methodology
1. Unit tests for individual tools
2. Integration tests for agent interactions
3. Edge case testing:
   - Nested operations
   - Invalid inputs
   - Transfer loops

### 6.2 Debugging Tools
```python
def debug_stream(graph, input):
    for chunk in graph.stream(input):
        print(f"=== {chunk.node} ===")
        print_messages(chunk.messages)
```

## 7. Future Improvements

1. **Dynamic Agent Registration**
2. **Advanced Routing Logic**
3. **Performance Monitoring**
4. **Multi-modal Support**

## 8. Conclusion

This implementation demonstrates effective use of LangChain's tooling system combined with LangGraph's state management capabilities. The system shows:

- Robust inter-agent collaboration
- Clear separation of concerns
- Maintainable architecture
- Extensible design patterns

The iterative development process highlighted the importance of:
- Precise prompt engineering
- Strict type safety
- Comprehensive tool handling
- Systematic state management

This documentation serves as both implementation guide and architectural reference for future extensions of the system.