# Project Status

[← Back to Main Documentation](../../../../README.md)

## Template Item

| Feature        | Status               | Note                   | Todo                                             | Ref                                  |
| -------------- | -------------------- | ---------------------- | ------------------------------------------------ | ------------------------------------ |
| [Feature Name] | [✅\|🔄\|🚧\|⚠️\|❌] | [Brief status context] | - [Primary todo item]<br>- [Secondary todo item] | [Multiple reference types supported] |

Legend:

- ✅ Implemented: Feature is complete and deployed
- 🔄 Optimization: Feature is deployed but being improved/optimized
- 🚧 In Progress: Feature is currently being developed
- ⚠️ Partial: Feature is partially implemented
- ❌ Not Started: Feature development hasn't begun yet

Guidelines for filling the template:

- Feature: Clear, concise name of the feature/capability
- Status: Select one of the four status indicators
- Note: Brief context about current status/blockers/achievements
- Todo: List 2-3 specific, actionable items
- Ref: Flexible reference field that can include:
  - Issue/ticket links (e.g., "JIRA-123", "github.com/org/repo/issues/123")
  - Documentation links (e.g., "docs/api.md#auth", "wiki/Feature-Spec")
  - Code references (e.g., "src/auth/login.js", "PR #456")
  - Notes or comments (e.g., "Blocked by API upgrade", "See team discussion 12/25")
  - Technical specifications (e.g., "RFC-123", "Design Doc v2")
  - Multiple references (separate with commas)

## Project Features Implementation Status

| Feature                     | Status               | Notes                                                             | ToDo Items                                                                                                   | References                                                                                                                   |
| --------------------------- | -------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| RAG Integration             | 🔄                   | Basic algorithm implemented                                       | - Enhance data ingestion pipeline<br>- Optimize retrieval mechanisms<br>- Implement agentic RAG capabilities | - `apps/dev/frameworks/LlamaIndex/data.ipynb`<br>- `apps/features/rag`                                                       |
| Control Agent               | 🔄                   | Core functionality operational                                    | - Optimize performance metrics<br>- Evaluate LLM engine alternatives<br>- Streamline LLM pipeline calls      | - `apps/features/agents/car/dev.ipynb/Agent/Car Operator`<br>- `apps/features/agents/car/apis.py`                            |
| Map Agent                   | 🚧                   | Core functionality implemented; pending integration               | - Complete main agentic workflow integration<br>- Perform integration testing                                | - https://www.mapbox.com/<br>- `apps/features/agents/car/dev.ipynb/Agent/Navigation`<br>- `apps/features/agents/car/apis.py` |
| Infotainment Agent          | 🚧                   | Child services under development                                  | - Complete main agentic workflow integration<br>- Perform integration testing                                |                                                                                                                              |
| Music Service               | 🔄                   | Infotainment Agent component                                      | - Refactor for optimal performance<br>- Implement caching mechanism                                          | - https://www.youtube.com/<br>-`apps/services/music`                                                                         |
| Search Service              | 🔄                   | Infotainment Agent component                                      | - Optimize search algorithms<br>- Implement request throttling                                               | - https://tavily.com/<br>- `apps/services/search`                                                                            |
| Weather Service             | 🔄                   | Infotainment Agent component                                      | - Implement data caching<br>- Optimize API usage                                                             | - https://open-meteo.com/<br>- `apps/services/weather`                                                                       |
| Speech-to-Text Service      | ✅                   | - Whisper.cpp integration complete<br>- Riva integration complete | - Expand language support (Japanese, Korean)                                                                 | - https://github.com/ggerganov/whisper.cpp<br>- `apps/services/audio`                                                        |
| Text-to-Speech Service      | ✅                   | - Piper integration complete                                      | - Expand language support (Japanese, Korean)                                                                 | - https://github.com/rhasspy/piper<br>- `apps/services/audio`                                                                |
| Wake-Word Detection Service | ✅                   | - OpenWakeWord integration complete                               | - Train models with diverse audio samples                                                                    | - https://github.com/dscripka/openWakeWord<br>- `apps/services/audio`                                                        |
| [Feature Name]              | [✅\|🔄\|🚧\|⚠️\|❌] | [Brief status context]                                            | - [Primary todo item]<br>- [Secondary todo item]                                                             | [Multiple reference types supported]                                                                                         |

## System Capabilities Status

| Feature        | Status               | Note                   | Todo                                             | Ref                                  |
| -------------- | -------------------- | ---------------------- | ------------------------------------------------ | ------------------------------------ |
| [Feature Name] | [✅\|🔄\|🚧\|⚠️\|❌] | [Brief status context] | - [Primary todo item]<br>- [Secondary todo item] | [Multiple reference types supported] |
