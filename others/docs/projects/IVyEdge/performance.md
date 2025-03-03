# Performance

## Agents

### RAG

Query

```text
What are the main safety procedures to follow before driving the vehicle?
```

Response

```text
You're looking for guidance on how to handle various driving scenarios, such as turning off the engine whiledriving, using the parking brake, and operating the lights and wipers. It's generally recommended to turn offthe engine when not in use or if you need to stop suddenly, especially on slippery roads where stability may be compromised. Additionally, it's a good idea to check your surroundings before opening or closing doors, asstrong winds can blow them open unexpectedly.
```

Time to first token: 

Total time: 
- Ollama, CPU: 1m35s
- Ollama, GPU:
    - Separate: 7.2s
    - Multi-agents: 9.1s

### Control

Query

```text
What's the current fan speed?
```

Response

```text
The fan speed is currently set to 2.
```

Time to first token: 

Total time:
- Ollama, CPU: 24s
- Ollama, GPU:
    - Separate: 2.4s
    - Multi-agents: 2.9s

---

Query

```text
Set the driver's temperature to 23 degrees
```

Response

```text

```

Time to first token: 
Total time:
- Ollama, CPU: 1m6s
- Ollama, GPU:
    - Separate: 3s
    - Multi-agents: 
 
### Navigation

Query

```text
Tìm quán cháo vịt quanh đây
```

Response

```text
The current navigation result is successful, and the search action has been completed with 5 matching places.
```

Time to first token: 

Total time:
- Ollama, CPU: 
- Ollama, GPU:
    - Separate: 4s
    - Multi-agents: 5.1s

---

Query

```text
Chỉ đường đến Quán cháo vịt Thanh đa
```

Response

```text

```

Time to first token:

Total time:
- Ollama, GPU:
    - Separate: 2s
    - Multi-agents: 

## Features

### Speech to text

Input:

```text

```

Total time:

### Text to speech

Input:

```text

```

Total time:
