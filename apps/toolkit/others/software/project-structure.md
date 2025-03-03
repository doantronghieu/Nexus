```text
project_root/                                      # Root project directory
├── .env.example                                # Root-level example env file with common variables
├── .github/                                       # GitHub configurations
│   ├── workflows/                                 # CI/CD workflows
│   │   ├── ci.yml                                # Continuous Integration configuration
│   │   ├── cd.yml                                # Continuous Deployment configuration
│   │   ├── dependency-check.yml                  # Dependency vulnerability scanning
│   │   └── security-scan.yml                     # Security scanning workflow
│   ├── CODEOWNERS                                # Code ownership assignments
│   └── pull_request_template.md                  # PR template with review checklist
├── docs/                                         # Documentation root
│   ├── architecture/                             # Architecture documentation
│   │   ├── decisions/                            # Architecture Decision Records (ADRs)
│   │   │   ├── template.md                       # ADR template
│   │   │   └── [date]_[decision].md              # Example: 20240101_event_sourcing.md, 20240115_cqrs_implementation.md, 20240130_rag_architecture.md
│   │   └── diagrams/                             # Architecture diagrams
│   │       └── [component]_diagram.[ext]          # Example: event_flow.png, rag_components.svg, service_topology.svg
│   ├── api/                                      # API documentation
│   │   ├── standards/                            # API design standards
│   │   │   ├── naming.md                         # Naming conventions
│   │   │   ├── versioning.md                     # Versioning strategy
│   │   │   └── responses.md                      # Standard response formats
│   │   ├── examples/                             # API usage examples
│   │   └── [version]/                            # Version-specific documentation
│   │       └── openapi.yaml                      # OpenAPI/Swagger specification
│   └── guides/                                   # Development guides
│       ├── setup.md                              # Setup instructions
│       ├── development.md                        # Development guidelines
│       └── deployment.md                         # Deployment procedures
├── backend/                                      # Backend services root
│   ├── shared/                                   # Shared components
│   │   ├── .env.[environment]                  # Example: .env.dev, .env.prod - Shared component configurations across all services
│   │   ├── core/                                 # Core framework components
│   │   │   ├── config/                           # Configuration management
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_settings.py              # Base settings class
│   │   │   │   ├── defaults.py                   # Default configuration values
│   │   │   │   └── [env]_settings.py             # Environment-specific settings
│   │   │   ├── security/                         # Security components
│   │   │   │   ├── __init__.py
│   │   │   │   ├── authentication.py             # Authentication handlers
│   │   │   │   ├── authorization.py              # Authorization handlers
│   │   │   │   └── encryption.py                 # Encryption utilities
│   │   │   └── observability/                    # Observability components
│   │   │       ├── __init__.py
│   │   │       ├── logging_config.py             # Logging configuration
│   │   │       ├── metrics_config.py             # Metrics configuration
│   │   │       └── tracing_config.py             # Distributed tracing
│   │   ├── algorithms/                           # Shared algorithm components
│   │   │   ├── __init__.py
│   │   │   ├── interfaces/                       # Algorithm interfaces
│   │   │   │   ├── __init__.py
│   │   │   │   └── i_[algorithm_type].py         # Example: i_vector_store.py, i_text_splitter.py, i_embedder.py
│   │   │   └── base/                             # Base algorithm classes
│   │   │       ├── __init__.py
│   │   │       └── base_[algorithm_type].py      # Example: base_vector_store.py, base_text_splitter.py, base_embedder.py
│   │   ├── utils/                                # Shared utilities
│   │   │   ├── __init__.py
│   │   │   └── [utility_type].py                 # Example: datetime_utils.py, string_utils.py, validation_utils.py
│   │   └── test_utils/                           # Shared test utilities
│   │       ├── __init__.py
│   │       ├── fixtures.py                       # Common test fixtures
│   │       └── factories.py                      # Common test factories
│   │
│   ├── domains/                                  # Domain services
│   │   └── [domain_name]/                        # Example: llm_service/, order_service/, vehicle_service/
│   │       ├── pyproject.toml                    # Domain service dependencies
│   │       ├── setup.cfg                         # Python package configuration
│   │       ├── .env.example                    # Domain-specific example env file
│   │       ├── .env.[environment]              # Example - LLM: OPENAI_API_KEY, MODEL_NAME | E-commerce: STRIPE_KEY, INVENTORY_DB | Automotive: TELEMETRY_URL, SENSOR_KEY
│   │       ├── Dockerfile                        # Service Dockerfile
│   │       ├── README.md                         # Service documentation
│   │       └── src/                              # Service source code
│   │           ├── main.py                       # Service entry point
│   │           ├── config.py                     # Service configuration
│   │           ├── constants.py                  # Service constants
│   │           ├── exceptions.py                 # Service exceptions
│   │           │
│   │           ├── domain/                       # Domain layer (Core)
│   │           │   ├── models/                   # Domain models
│   │           │   │   ├── __init__.py
│   │           │   │   ├── base_model.py         # Base domain model
│   │           │   │   └── [entity].py           # Example - LLM: prompt.py, completion.py | E-commerce: order.py, product.py | Automotive: vehicle.py, maintenance.py
│   │           │   ├── events/                  # Domain events
│   │           │   │   ├── __init__.py
│   │           │   │   ├── base_event.py        # Base event class
│   │           │   │   ├── definitions/         # Event definitions
│   │           │   │   │   └── [entity]_[event].py      # Example - LLM: completion_generated.py | E-commerce: order_placed.py | Automotive: service_completed.py
│   │           │   │   └── handlers/            # Event handlers
│   │           │   │       └── [event]_handler.py       # Example - LLM: model_updated_handler.py | E-commerce: inventory_updated_handler.py | Automotive: maintenance_scheduled_handler.py
│   │           │   ├── algorithms/               # Domain-specific algorithms
│   │           │   │   ├── __init__.py
│   │           │   │   ├── interfaces/           # Algorithm interfaces
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── i_[algorithm].py  # Example - LLM: i_rag.py, i_prompt_builder.py | E-commerce: i_recommendation.py | Automotive: i_diagnostic.py
│   │           │   │   ├── base/                # Base algorithm implementations
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── base_[algorithm].py  # Example - LLM: base_rag.py, base_prompt_builder.py | E-commerce: base_recommendation.py
│   │           │   │   └── implementations/     # Concrete algorithm implementations
│   │           │   │       ├── __init__.py
│   │           │   │       └── [algorithm_type]/ # Algorithm variants
│   │           │   │           ├── __init__.py
│   │           │   │           └── [variant].py  # Example - LLM: basic_rag.py, graph_rag.py, hybrid_rag.py | E-commerce: collaborative_filtering.py, content_based.py
│   │           │   ├── services/                # Domain services
│   │           │   │   ├── __init__.py
│   │           │   │   └── [entity]_service.py  # Example - LLM: completion_service.py, embedding_service.py | E-commerce: order_service.py
│   │           │   └── value_objects/           # Value objects
│   │           │       ├── __init__.py
│   │           │       └── [name]_vo.py         # Example - LLM: token_count_vo.py | E-commerce: money_vo.py | Automotive: mileage_vo.py
│   │           │
│   │           ├── application/                  # Application layer (Incoming Ports)
│   │           │   ├── api/                      # API definitions
│   │           │   │   ├── v[version]/           # API version
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── router.py         # Version router
│   │           │   │   │   ├── dependencies.py   # Endpoint dependencies
│   │           │   │   │   └── endpoints/        # Route handlers
│   │           │   │   │       └── [feature]_routes.py  # Example - LLM: completion_routes.py | E-commerce: order_routes.py | Automotive: diagnostic_routes.py
│   │           │   ├── interfaces/               # Incoming ports (interfaces)
│   │           │   │   ├── __init__.py
│   │           │   │   ├── i_[feature]_usecase.py  # Example - LLM: i_completion_usecase.py | E-commerce: i_checkout_usecase.py
│   │           │   │   └── i_[feature]_query.py    # Example - LLM: i_model_query.py | E-commerce: i_inventory_query.py
│   │           │   ├── usecases/                # Use case implementations
│   │           │   │   └── [feature]/           # Feature-specific use cases
│   │           │   │       ├── __init__.py
│   │           │   │       ├── commands/        # Command handlers
│   │           │   │       │   └── [command]_handler.py  # Example - LLM: generate_completion_handler.py | E-commerce: place_order_handler.py
│   │           │   │       └── queries/         # Query handlers
│   │           │   │           └── [query]_handler.py    # Example - LLM: get_model_status_handler.py | E-commerce: get_cart_handler.py
│   │           │   └── dtos/                    # Data Transfer Objects
│   │           │       ├── requests/            # Request DTOs
│   │           │       │   └── [feature]_request.py   # Example - LLM: completion_request.py | E-commerce: order_request.py
│   │           │       └── responses/           # Response DTOs
│   │           │           └── [feature]_response.py  # Example - LLM: completion_response.py | E-commerce: order_response.py
│   │           │
│   │           └── infrastructure/              # Infrastructure layer (Outgoing Adapters)
│   │               ├── singletons/                        # Centralized singleton management
│   │               │   ├── __init__.py
│   │               │   ├── base_singleton.py              # Base singleton implementation with metaclass
│   │               │   ├── definitions/                   # Singleton class definitions
│   │               │   │   ├── __init__.py
│   │               │   │   ├── db_singleton.py            # Example: Database connection singleton
│   │               │   │   ├── cache_singleton.py         # Example: Cache manager singleton
│   │               │   │   └── config_singleton.py        # Example: Configuration singleton
│   │               │   ├── registry.py                    # Singleton instance registry
│   │               │   └── initialization.py              # Singleton initialization orchestration
│   │               │
│   │               ├── startup/                           # Add singleton initialization to startup
│   │               │   ├── __init__.py
│   │               │   └── singleton_initializer.py        # Handles singleton initialization order
│   │               │
│   │               ├── factories/
│   │               │   ├── [entity]_factory.py
│   │               │   └── abstract_factory.py
│   │               │
│   │               ├── adapters/                # Adapter implementations
│   │               │   ├── persistence/         # Data persistence
│   │               │   │   ├── __init__.py
│   │               │   │   ├── base_repository.py     # Base repository with common operations
│   │               │   │   ├── repositories/          # Repository implementations
│   │               │   │   │   ├── __init__.py
│   │               │   │   │   └── [entity]_repository.py  # Example - LLM: prompt_repository.py | E-commerce: order_repository.py
│   │               │   │   └── models/               # Database models
│   │               │   │       ├── __init__.py
│   │               │   │       ├── base_model.py        # Base model with common fields
│   │               │   │       ├── mixins/              # Model mixins
│   │               │   │       │   ├── __init__.py
│   │               │   │       │   └── [mixin_type]_mixin.py  # Example: timestamp_mixin.py, soft_delete_mixin.py, audit_mixin.py
│   │               │   │       └── [entity]_model.py # Example - LLM: completion_model.py | E-commerce: product_model.py
│   │               │   ├── [service_type]/      # Service type adapters
│   │               │   │   ├── __init__.py
│   │               │   │   ├── base_[service].py         # Example: base_llm.py, base_vectorstore.py - Abstract base classes
│   │               │   │   └── providers/                # Provider-specific implementations
│   │               │   │       ├── __init__.py
│   │               │   │       └── [provider]_[service].py # Example LLM: openai_llm.py, anthropic_llm.py | Example Vectorstore: qdrant_vectorstore.py, pinecone_vectorstore.py
│   │               │   ├── algorithms/          # Algorithm implementations
│   │               │   │   ├── __init__.py
│   │               │   │   ├── config/          # Algorithm configurations
│   │               │   │   │   ├── __init__.py
│   │               │   │   │   └── [algorithm]_config.py  # Example - LLM: rag_config.py, embedding_config.py | E-commerce: recommender_config.py
│   │               │   │   └── providers/       # Third-party algorithm implementations
│   │               │   │       ├── __init__.py
│   │               │   │       └── [provider]/  # Provider-specific implementations
│   │               │   │           ├── __init__.py
│   │               │   │           └── [algorithm]_impl.py  # Example - LLM: langchain_rag.py, llama_index_rag.py | E-commerce: scikit_recommender.py
│   │               │   ├── messaging/           # Message broker adapters
│   │               │   │   ├── __init__.py
│   │               │   │   ├── base_messaging.py         # Base messaging class
│   │               │   │   └── providers/               # Message broker implementations
│   │               │   │       ├── __init__.py
│   │               │   │       └── [broker]_provider/   # Broker-specific implementation
│   │               │   │           ├── __init__.py
│   │               │   │           ├── config.py        # Broker configuration
│   │               │   │           ├── connection.py    # Connection management
│   │               │   │           ├── consumer.py      # Message consumer # Example: kafka_consumer.py, rabbitmq_consumer.py
│   │               │   │           └── publisher.py     # Message publisher # Example: kafka_publisher.py, rabbitmq_publisher.py
│   │               │   └── external/            # External service adapters
│   │               │       ├── __init__.py
│   │               │       ├── base_client.py           # Base external client
│   │               │       ├── [service_name]/          # Service-specific client implementation
│   │               │       │   ├── __init__.py
│   │               │       │   ├── client.py            # Service client # Example - LLM: openai_client.py | E-commerce: stripe_client.py
│   │               │       │   ├── config.py            # Client configuration
│   │               │       │   ├── models.py            # Client data models
│   │               │       │   └── exceptions.py        # Client-specific exceptions
│   │               │       └── utils/                   # Client utilities
│   │               │           └── [utility_name].py    # Example: retry_handler.py, rate_limiter.py, circuit_breaker.py
│   │               └── ports/                   # Outgoing ports (interfaces)
│   │                   ├── __init__.py
│   │                   ├── i_[service].py              # Example - LLM: i_llm.py, i_embedding.py | E-commerce: i_payment.py
│   │                   └── i_[service]_provider.py     # Example - LLM: i_llm_provider.py | E-commerce: i_payment_provider.py
│   ├── gateway/                                 # API Gateway service
│   │   ├── .env.example                        # Gateway example env file
│   │   ├── .env.[environment]                  # Example: AUTH_SECRET, RATE_LIMIT_CONFIG, CORS_ORIGINS
│   │   ├── src/                                # Gateway source code
│   │   │   ├── main.py                         # Gateway entry point
│   │   │   ├── config/                         # Gateway configuration
│   │   │   │   ├── __init__.py
│   │   │   │   └── settings.py                 # Gateway settings
│   │   │   ├── routes/                         # Route definitions
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_router.py              # Base router implementation
│   │   │   │   └── [domain]_routes.py          # Example: llm_routes.py (completions, embeddings) | commerce_routes.py (orders, products) | automotive_routes.py (diagnostics, maintenance)
│   │   │   ├── middleware/                     # Gateway middleware
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_middleware.py          # Base middleware class
│   │   │   │   └── [middleware_type].py        # Example: auth_middleware.py (JWT validation) | rate_limit_middleware.py (request throttling) | tracing_middleware.py (request tracing)
│   │   │   ├── transformers/                   # Response transformers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_transformer.py         # Base transformer class
│   │   │   │   └── [transform_type]_transformer.py  # Example: json_transformer.py, xml_transformer.py, protobuf_transformer.py
│   │   │   └── policies/                       # Gateway policies
│   │   │       ├── __init__.py
│   │   │       ├── base_policy.py              # Base policy class
│   │   │       └── [policy_type].py            # Example: circuit_breaker_policy.py (failure handling) | retry_policy.py (retry logic) | timeout_policy.py (request timeouts)
│   │   └── config/                             # Gateway configuration
│   │       └── routes.yaml                     # Route configurations
│   │
│   └── event_bus/                              # Event bus service
│       ├── .env.example                        # Event bus example env file
│       ├── .env.[environment]                  # Example: KAFKA_BROKERS, RABBITMQ_URL, REDIS_URL
│       ├── src/                                # Event bus source code
│       │   ├── main.py                         # Event bus entry point
│       │   ├── config/                         # Event bus configuration
│       │   │   ├── __init__.py
│       │   │   └── settings.py                 # Event bus settings
│       │   ├── brokers/                        # Message broker integrations
│       │   │   ├── __init__.py
│       │   │   ├── base_broker.py              # Base broker interface
│       │   │   └── [broker_name]/              # Broker implementation
│       │   │       ├── __init__.py
│       │   │       ├── config.py               # Broker config # Example: kafka_config.py (topic configs) | rabbitmq_config.py (exchange settings)
│       │   │       ├── client.py               # Broker client # Example: kafka_client.py (producer/consumer) | rabbitmq_client.py (publisher/subscriber)
│       │   │       └── handlers.py             # Broker handlers # Example: kafka_handler.py (message handling) | rabbitmq_handler.py (message processing)
│       │   ├── streams/                        # Event streams
│       │   │   ├── __init__.py
│       │   │   ├── base_stream.py             # Base stream processor
│       │   │   └── [stream_type]/             # Stream implementation
│       │   │       ├── __init__.py
│       │   │       ├── processor.py            # Stream processor # Example: completion_stream.py (LLM completions) | order_stream.py (order processing) | telemetry_stream.py (vehicle data)
│       │   │       └── handlers.py             # Stream handlers # Example: completion_handler.py (LLM results) | order_handler.py (order events) | telemetry_handler.py (sensor data)
│       │   └── processors/                     # Event processors
│       │       ├── __init__.py
│       │       ├── base_processor.py           # Base event processor
│       │       └── [event_type]_processor.py   # Example: llm_processor.py (completion events) | order_processor.py (order events) | diagnostic_processor.py (vehicle events)
│       └── config/
│           └── topics.yaml                     # Topic configurations
│
└── devops/                                     # Infrastructure and operations
    ├── docker/                                 # Container configurations
    │   ├── base/                               # Base Docker configurations
    │   │   ├── Dockerfile.[type]               # Example types: base, dev, gpu, test | Example: Dockerfile.base: python:3.10-slim, Dockerfile.gpu: nvidia/cuda:11.8.0-runtime
    │   │   └── requirements/                   # Base requirements
    │   │       └── requirements.[type].txt     # Example: requirements.base.txt (fastapi,uvicorn) | requirements.dev.txt (pytest,black) | requirements.gpu.txt (torch,transformers)
    │   │
    │   ├── services/                           # Service-specific Dockerfiles
    │   │   └── [service_name]/                 # Example: llm_inference/, vector_store/, embedding/
    │   │       ├── .env.[environment]          # Example: .env.dev (development configs), .env.test (testing configs)
    │   │       ├── Dockerfile.[type]           # Example - LLM: base:python-gpu (inference), dev:hot-reload (development) | Vector Store: base:python-slim (qdrant), dev:debug (development)
    │   │       └── requirements.[type].txt     # Example - LLM: torch,transformers,accelerate | Vector Store: qdrant-client,faiss-cpu
    │   │
    │   ├── domains/                            # Domain service Dockerfiles
    │   │   └── [domain_name]/                  # Example: llm/, commerce/, automotive/
    │   │       ├── Dockerfile.[type]           # Example - LLM: base:fastapi, dev:debug | E-commerce: base:python-slim, prod:optimized
    │   │       └── requirements.[type].txt     # Example - LLM: openai,anthropic | E-commerce: stripe,paypal | Automotive: can-utils,obd
    │   │
    │   ├── gateway/                            # Gateway Dockerfiles
    │   │   └── Dockerfile.[type]               # Example: base:nginx, dev:debug-enabled, prod:alpine
    │   │
    │   └── compose/                            # Docker Compose configurations
    │       ├── base/                           # Base compose files
    │       │   └── docker-compose.[type].yml   # Example: base.yml (shared services) | deps.yml (dependencies) | monitoring.yml (observability)
    │       │
    │       ├── development/                    # Development environment
    │       │   └── docker-compose.[type].yml   # Example: dev.yml (hot reload) | tools.yml (pgadmin,redis-commander) | debug.yml (debugging)
    │       │
    │       ├── testing/                        # Testing environment
    │       │   └── docker-compose.[type].yml   # Example: test.yml (pytest) | coverage.yml (code coverage) | integration.yml (integration tests)
    │       │
    │       └── local/                          # Local development support
    │           ├── .env.[component]            # Example: .env.postgres (DB configs), .env.redis (cache configs)
    │           ├── infrastructure/             # Infrastructure services
    │           │   └── docker-compose.[component].yml  # Example: postgres.yml (database) | redis.yml (cache) | rabbitmq.yml (message queue)
    │           │
    │           ├── services/                   # Service-specific compose files
    │           │   └── docker-compose.[service].yml  # Example: llm_inference.yml (GPU service) | vector_store.yml (Qdrant service)
    │           │
    │           └── providers/                  # External service mocks/emulators
    │               └── docker-compose.[provider].yml  # Example: openai_mock.yml (LLM API) | stripe_mock.yml (payments) | telemetry_mock.yml (vehicle data)
    │
    ├── kubernetes/                             # Kubernetes manifests
    │   ├── base/                               # Base configurations
    │   │   ├── deployments/                    # Deployment definitions
    │   │   │   └── [service]_deployment.yaml   # Example: llm_service.yaml (inference deployment) | order_service.yaml (order processing)
    │   │   ├── services/                       # Service definitions
    │   │   │   └── [service]_service.yaml      # Example: llm_service.yaml (inference service) | order_service.yaml (order API)
    │   │   └── ingress/                        # Ingress rules
    │   │       └── [domain]_ingress.yaml       # Example: api_ingress.yaml (API gateway) | monitoring_ingress.yaml (dashboards)
    │   └── overlays/                           # Environment overlays
    │       └── [environment]/                  # Example: development/, staging/, production/
    │           └── kustomization.yaml          # Environment-specific configurations
    │
    ├── terraform/                              # Infrastructure as Code
    │   ├── modules/                            # Terraform modules
    │   │   └── [resource]/                     # Example: database/, cache/, compute/
    │   │       ├── main.tf                     # Resource configuration
    │   │       ├── variables.tf                # Input variables
    │   │       └── outputs.tf                  # Output definitions
    │   └── environments/                       # Environment configurations
    │       └── [environment]/                  # Example: dev/, stage/, prod/
    │           ├── main.tf                     # Environment configuration
    │           └── terraform.tfvars            # Environment variables
    │
    └── monitoring/                             # Monitoring setup
        ├── prometheus/                         # Prometheus configuration
        │   └── rules/                          # Alert rules
        │       └── [alert_type]_rules.yml      # Example: service_alerts.yml (API alerts) | model_alerts.yml (ML alerts)
        └── grafana/                            # Grafana configuration
            └── dashboards/                     # Dashboard definitions
                └── [domain]_dashboard.json     # Example: llm_metrics.json (model perf) | order_metrics.json (business KPIs)
```