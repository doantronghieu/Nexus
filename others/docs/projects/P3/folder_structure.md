# Directory Structure

```
.
├── Makefile                                        # Project build/deployment rules
├── README.md                                       # Project documentation
├── apps                                            # Application code
│   ├── clients                                     # Utils clients for interacting with services
│   ├── context                                     # Contexts for the app
│   │   ├── __init__.py                             # Empty init file
│   │   ├── app                                     # (Not visible in provided code)
│   │   ├── configs                                 # Configuration-related modules 
│   │   │   ├── __init__.py                         # Empty package init file
│   │   │   ├── llm.py                              # Minimal imports for LLM configuration
│   │   │   ├── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   │   └── rich.py                             # Rich text formatting themes and console
│   │   ├── consts                                  # Constants used across the application
│   │   │   ├── __init__.py                         # Empty package init file
│   │   │   └── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   ├── external                                # External integrations (mostly empty)
│   │   │   └── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   ├── infra                                   # Infrastructure configuration
│   │   │   ├── clients.py                          # Client instances for Qdrant, MongoDB, Redis
│   │   │   ├── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   │   ├── services_info.py                    # Service URLs, hosts and ports config
│   │   │   └── storages.py                         # Empty file, likely for storage definitions
│   │   ├── instances                               # Instantiated components
│   │   │   ├── __init__.py                         # Exports LLM and vector store instances
│   │   │   ├── llms.py                             # Creates LLM instances based on settings
│   │   │   ├── main.py                             # Empty file, likely for main instances
│   │   │   ├── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   │   └── vector_stores.py                    # Creates vector store instances based on settings
│   │   ├── models                                  # Data model definitions
│   │   │   ├── __init__.py                         # Empty package init file
│   │   │   └── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   ├── settings                                # Application settings
│   │   │   ├── __init__.py                         # Empty package init file
│   │   │   ├── main.py                             # Core settings: LLM framework, models, vector stores
│   │   │   └── packages.py                         # Path setup & env loading (DUPLICATED)
│   │   └── utils                                   # Utility functions and helpers
│   │       ├── __init__.py                         # Empty package init file
│   │       ├── consts.py                           # Terminal colors and emojis for logging
│   │       ├── handlers.py                         # Simple print handler utility
│   │       ├── packages.py                         # Path setup & env loading (DUPLICATED)
│   │       └── typer.py                            # Type utilities, enum helpers, dataclasses
│   ├── data                                        # Application data
│   │   ├── org                                     # Organization data
│   │   ├── processed                               # Processed data
│   │   └── projects                                # Project-specific data
│   ├── dev                                         # Development utilities
│   │   ├── frameworks                              # Framework-specific utilities
│   │   └── tech                                    # Technology-specific utilities
│   ├── ports.env                                   # Port configuration environment file
│   ├── requirements                                # Python dependencies
│   ├── services                                    # Service implementations
│   │   ├── [service]                               # Generic service template
│   │   │   ├── server.py                           # Service server implementation
│   │   │   ├── packages.py                         # Dependencies for the service
│   │   │   ├── requirements.txt                    # Service-specific dependencies
│   │   │   └── templates                           # Service templates
│   │   │       └── index.html                      # Main template for the service
│   │   ├── [service-ai]                            # AI service template
│   │   │   ├── core.py                             # Core AI functionality
│   │   │   ├── dev.ipynb                           # Development notebook
│   │   │   ├── impl                                # Implementation details
│   │   │   │   ├── assets                          # Implementation assets
│   │   │   │   ├── packages.py                     # Implementation dependencies
│   │   │   │   ├── [repo]                          # Repository-related code
│   │   │   │   └── [impl].py                       # Implementation-specific code
│   │   │   ├── packages.py                         # AI service dependencies
│   │   │   ├── requirements.txt                    # AI service dependencies list
│   │   │   ├── server.py                           # AI service server
│   │   │   ├── utils.py                            # AI service utilities
│   │   │   └── templates                           # AI service templates
│   │   │       └── ui.html                         # AI service UI
│   │   ├── bases                                   # Base service implementations
│   │   │   ├── ai.py                               # Base AI service
│   │   │   ├── example.py                          # Example base service
│   │   │   ├── packages.py                         # Base service dependencies
│   │   │   ├── server.py                           # Base server implementation
│   │   │   ├── service.py                          # Base service implementation
│   │   │   ├── static                              # Static assets for base services
│   │   │   └── templates                           # Base service templates
│   │   │       ├── index.html                      # Main template
│   │   │       └── websocket.html                  # WebSocket template
│   │   └── llm                                     # LLM services
│   │       └── agents                              # LLM agents
│   │           ├── __init__.py                     # Agents initialization
│   │           └── [project]                       # Project-specific agents
│   │               ├── __init__.py                 # Project agent initialization
│   │               ├── packages.py                 # Project agent dependencies
│   │               ├── prompts.yaml                # Agent prompts
│   │               ├── child                       # Child agents
│   │               │   └── [child_agent].py        # Child agent implementation
│   │               ├── context.py                  # Agent context
│   │               ├── dev.ipynb                   # Development notebook
│   │               ├── manager.py                  # Agent manager
│   │               ├── packages.py                 # Agent dependencies
│   │               ├── prompts.yaml                # Agent prompts
│   │               ├── server.py                   # Agent server
│   │               └── tools                       # Agent tools
│   │                   ├── __init__.py             # Tools initialization
│   │                   ├── main.py                 # Main tools
│   │                   ├── [tool].py               # Specific tool implementation
│   │                   └── packages.py             # Tool dependencies
│   └── toolkit                                     # Reusable toolkit packages
│       └── [technology]                            # Technology-specific tools (langchain, langgraph, etc.)
├── data                                            # Project data
│   ├── assets                                      # Project assets
│   └── docker                                      # Docker volume data
│       └── [container_volume]                      # Container-specific volume data
├── devops                                          # DevOps configuration
│   ├── docker                                      # Docker configuration
│   │   ├── {ServiceName}.Dockerfile                # Service-specific Dockerfiles
│   │   ├── apps                                    # App-specific Docker config
│   │   │   └── {app_name}.docker-compose.yaml      # App-specific docker-compose
│   │   ├── {environment}                           # Environment-specific Docker config
│   │   │   ├── {environment}.{tech}.Dockerfile     # Tech-specific Dockerfile for environment
│   │   │   ├── {environment}.{tech}.docker-compose.yaml # Environment docker-compose
│   │   │   └── {service_name}.docker-compose.yaml  # Service-specific docker-compose
│   │   ├── data                                    # Docker data
│   │   │   ├── database.{format}                   # Database files
│   │   │   ├── config.{format}                     # Configuration files
│   │   │   └── logs                                # Log files
│   │   │       ├── {service}_access.log            # Service access logs
│   │   │       └── {service}_error.log             # Service error logs
│   │   ├── infra                                   # Infrastructure Docker config
│   │   │   ├── docker-compose.yaml                 # Main infrastructure docker-compose
│   │   │   └── {service}.docker-compose.yaml       # Service-specific docker-compose
│   │   ├── {platform}                              # Platform-specific Docker config
│   │   │   ├── {ServiceName}.{Technology}.Dockerfile # Service Dockerfile for platform
│   │   │   ├── {ServiceName}.{Technology}.docker-compose.yaml # Service compose for platform
│   │   │   ├── dev.Dockerfile                      # Development Dockerfile
│   │   │   └── dev.docker-compose.yaml             # Development docker-compose
│   │   ├── {category}                              # Category-specific Docker config
│   │   │   └── TODO                                # Placeholder for category config
│   │   ├── {service}.docker-compose.yaml           # Service-specific docker-compose
│   │   ├── services                                # Service Docker config
│   │   │   ├── {ServiceName}.Dockerfile            # Service-specific Dockerfile
│   │   │   ├── {category}                          # Category-specific services
│   │   │   │   ├── {ServiceName}.Dockerfile        # Category service Dockerfile
│   │   │   │   ├── {script_name}.sh                # Service scripts
│   │   │   │   └── {subcategory}                   # Subcategory services
│   │   │   │       └── {ServiceName}.Dockerfile    # Subcategory service Dockerfile
│   │   │   └── template.Dockerfile                 # Template Dockerfile
│   │   ├── services.docker-compose.yaml            # Main services docker-compose
│   │   ├── ui                                      # UI Docker config
│   │   │   └── {Framework}.{Component}.Dockerfile  # UI component Dockerfile
│   │   └── ui.docker-compose.yaml                  # UI docker-compose
│   ├── helm                                        # Helm charts
│   │   ├── Chart.yaml                              # Helm chart definition
│   │   ├── charts                                  # Subchart directory
│   │   │   └── {placeholder}.txt                   # Placeholder for subcharts
│   │   ├── templates                               # Helm templates
│   │   │   ├── NOTES.txt                           # Helm notes
│   │   │   ├── _helpers.tpl                        # Helm helpers
│   │   │   ├── deployment.yaml                     # Deployment template
│   │   │   ├── hpa.yaml                            # Horizontal Pod Autoscaler
│   │   │   ├── ingress.yaml                        # Ingress template
│   │   │   ├── service.yaml                        # Service template
│   │   │   ├── serviceaccount.yaml                 # Service account template
│   │   │   └── tests                               # Template tests
│   │   │       └── test-connection.yaml            # Connection test
│   │   └── values.yaml                             # Helm values
│   ├── infra                                       # Infrastructure config
│   │   └── infra.yaml                              # Infrastructure definition
│   ├── k8s                                         # Kubernetes config
│   │   ├── config_map.yaml                         # ConfigMap
│   │   ├── deployment.yaml                         # Deployment
│   │   ├── hpa.yaml                                # Horizontal Pod Autoscaler
│   │   ├── ingress.yaml                            # Ingress
│   │   ├── service.yaml                            # Service
│   │   └── volume.yaml                             # Volume
│   ├── mks                                         # Make scripts
│   │   ├── {service}.mk                            # Service-specific make scripts
│   │   └── setup.mk                                # Setup make script
│   ├── scripts                                     # Utility scripts
│   │   ├── cleanup                                 # Cleanup scripts
│   │   │   └── {cleanup_task}.sh                   # Specific cleanup tasks
│   │   ├── cleanup.sh                              # Main cleanup script
│   │   ├── dev.sh                                  # Development script
│   │   ├── install                                 # Installation scripts
│   │   │   └── {package}.sh                        # Package installation
│   │   ├── {script_name}.sh                        # Utility scripts
│   │   ├── repos                                   # Repository scripts
│   │   │   ├── {repo_name}                         # Repository-specific scripts
│   │   │   │   ├── {repo_name}.sh                  # Main repository script
│   │   │   │   └── {component}                     # Component-specific scripts
│   │   │   │       ├── {file_name}.py              # Python utility for component
│   │   │   │       ├── {component}.sh              # Component script
│   │   │   │       └── {file_name}.txt             # Component notes/docs
│   │   │   └── {repo_name}                         # Another repository
│   │   │       ├── {script_name}.sh                # Repository script
│   │   │       └── {script_name}.py                # Repository Python utility
│   │   ├── setup                                   # Setup scripts
│   │   │   ├── {environment}                       # Environment setup
│   │   │   │   └── {service}.sh                    # Service setup for environment
│   │   │   ├── {platform}.sh                       # Platform-specific setup
│   │   │   ├── repos                               # Repository setup
│   │   │   │   └── {repo}.sh                       # Repository setup script
│   │   │   └── {os}                                # OS-specific setup
│   │   │       └── {tool}.sh                       # Tool setup for OS
│   │   ├── setup.sh                                # Main setup script
│   │   ├── utils                                   # Utility scripts
│   │   │   ├── {utility_name}.py                   # Python utilities
│   │   │   ├── {utility_name}.sh                   # Shell utilities
│   │   │   └── setup.py                            # Utility setup
│   │   └── utils.sh                                # Main utilities script
│   └── setup                                       # Setup configuration
│       └── {service}                               # Service setup
│           ├── conf                                # Service configuration
│           │   └── {service}.conf                  # Service config file
│           ├── logs                                # Service logs
│           │   ├── access.log                      # Access logs
│           │   └── error.log                       # Error logs
│           ├── {service}-control.sh                # Service control script
│           ├── {service}.md                        # Service documentation
│           └── templates                           # Service templates
│               └── {framework}                     # Framework-specific templates
│                   ├── {Framework}.Template.Dockerfile # Framework template Dockerfile
│                   ├── config.{ext}                # Framework configuration
│                   └── {component}.docker-compose.yaml # Component docker-compose
├── front_end                                       # Frontend code
│   └── [project]                                   # Project-specific frontend
└── others                                          # Other resources
    └── docs                                        # Documentation
        └── projects                                # Project documentation
            └── [project]                           # Project-specific docs
```