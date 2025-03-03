e# Development Guide

[← Back to Main Documentation](../../../../README.md)

## Backend Components

### Application Structure

The application follows a standardized directory organization:

```text
/apps
├── dev/
│   └── frameworks/
│       └── [framework]/                  # AI frameworks (e.g., LangChain, LlamaIndex)
│           └── [component].[ipynb]       # Jupyter notebooks for experimenting with AI components
├── features/
│   ├── [feature]/
│   │   ├── base.py                       # Core interface that defines feature behavior
│   │   ├── impl/                         # Implementation directory
│   │   │   ├── [implementation].py       # Specific feature implementations
│   │   ├── dev.ipynb                     # Interactive development notebook for testing
│   │   └── apis.py                       # API endpoints for the feature
│   └── agents/
│       └── [agent]/                      # AI agent implementations (e.g., chat, search)
├── services/
│   └── [service]/
│       ├── base.py                       # Core service interface definition
│       ├── impl/
│   │   │   └── [implementation].py       # Different implementations of the service
│       ├── server.py                     # Web server setup (using FastAPI framework)
│       └── main.py                       # Shared service logic and API handlers
├── clients/
│   └── [service].py                      # Helper classes to interact with services
└── configs/                              # Application settings and environment configs
```

The configs directory serves as the single source of truth for all application settings and configurations.

Notes:

- In the notebook files, you can click on the toggle icon to collapse each section individually.

## Rules

- All configurations, constants, app components, and clients should be appropriately placed in the `context` folder.

### Containerization

#### Docker Configuration

Follow these container patterns:

- `devops/docker/services/[service].Dockerfile`
- `devops/docker/servers.docker-compose.yaml`: Application servers (Backend, Frontend)
- `devops/docker/services.docker-compose.yaml`: Common services

#### System Integration

Integrate using these build files:

- `devops/mks/services.mk`
- `Makefile`
- `devops/docker/docker-compose.yaml`

## Frontend Development

### Nuxt.js (Vue.js)

Setting up the development server:

```bash
cd front_end/{APP_NAME}
npm install
npm run dev
```
