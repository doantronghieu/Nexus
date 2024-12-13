# Project Structure

## 1. Root Level Organization

```plaintext
project_root/
├── shared/                          # Shared resources
├── mobile/                         # Flutter mobile application
├── backend/                        # FastAPI backend services
├── infrastructure/                 # Infrastructure and DevOps
├── tools/                          # Development tools
└── docs/                          # Project documentation

# Root Configuration
├── .editorconfig                   # Editor configuration
├── .gitignore                     # Git ignore patterns
├── docker-compose.yml             # Development environment setup
├── docker-compose.prod.yml        # Production environment setup
├── README.md                      # Project documentation
├── CHANGELOG.md                   # Version history
└── LICENSE                        # License information
```

## 2. Shared Layer

```plaintext
shared/
├── contracts/                      # Contract definitions
│   ├── bounded_contexts/          # DDD bounded contexts
│   │   └── [context_name]/
│   │       ├── entities/
│   │       ├── value_objects/
│   │       └── events/
│   │
│   ├── models/                    # Domain models
│   │   └── [feature]/
│   │       ├── entities/
│   │       │   ├── [entity].model.yaml
│   │       │   └── [entity].rules.yaml     # Validation rules
│   │       │
│   │       ├── value_objects/
│   │       │   ├── [vo].model.yaml
│   │       │   └── [vo].rules.yaml
│   │       │
│   │       └── enums/
│   │           └── [enum_name].enum.yaml
│   │
│   ├── api/                       # API contracts
│   │   ├── rest/
│   │   │   └── [feature]/
│   │   │       ├── commands/      # Command endpoints
│   │   │       │   └── [command_name]/
│   │   │       │       ├── request.yaml
│   │   │       │       └── response.yaml
│   │   │       │
│   │   │       └── queries/       # Query endpoints
│   │   │           └── [query_name]/
│   │   │               ├── request.yaml
│   │   │               └── response.yaml
│   │   │
│   │   └── graphql/
│   │       └── [feature]/
│   │           ├── types/
│   │           ├── queries/
│   │           └── mutations/
│   │
│   ├── events/                    # Event definitions
│   │   └── [feature]/
│   │       ├── domain/           # Domain events
│   │       │   ├── [event].event.yaml
│   │       │   └── [event].schema.yaml
│   │       │
│   │       ├── integration/      # Integration events
│   │       │   ├── [event].event.yaml
│   │       │   └── [event].schema.yaml
│   │       │
│   │       └── saga/            # Saga events
│   │           ├── commands/
│   │           │   └── [command].yaml
│   │           └── compensations/
│   │               └── [compensation].yaml
│   │
│   ├── sagas/                    # Saga definitions
│   │   └── [process]/
│   │       ├── orchestration/
│   │       │   ├── saga_definition.yaml
│   │       │   └── state_machine.yaml
│   │       │
│   │       └── compensation/
│   │           ├── failure_scenarios.yaml
│   │           └── recovery_actions.yaml
│   │
│   └── service_mesh/             # Service mesh contracts
│       ├── discovery/
│       │   ├── service_registry.yaml
│       │   └── endpoints.yaml
│       │
│       ├── resilience/
│       │   ├── circuit_breakers.yaml
│       │   └── rate_limits.yaml
│       │
│       └── routing/
│           ├── routes.yaml
│           └── policies.yaml
│
├── generators/                    # Code generation
│   ├── templates/
│   │   ├── flutter/
│   │   │   ├── entity.dart.jinja
│   │   │   ├── bloc.dart.jinja
│   │   │   └── repository.dart.jinja
│   │   │
│   │   └── python/
│   │       ├── entity.py.jinja
│   │       ├── command.py.jinja
│   │       └── query.py.jinja
│   │
│   └── scripts/
│       ├── generate_models.py
│       ├── generate_api.py
│       └── generate_events.py
│
└── generated/                     # Generated code
    ├── flutter/
    │   ├── models/
    │   │   └── [feature]/
    │   │       ├── entities/
    │   │       │   ├── [entity].dart
    │   │       │   ├── [entity].freezed.dart
    │   │       │   └── [entity].g.dart
    │   │       │
    │   │       └── value_objects/
    │   │           ├── [vo].dart
    │   │           └── [vo].freezed.dart
    │   │
    │   ├── api/
    │   │   └── [feature]/
    │   │       ├── commands/
    │   │       └── queries/
    │   │
    │   └── events/
    │       └── [feature]/
    │           ├── handlers/
    │           └── mappers/
    │
    └── python/
        ├── models/
        │   └── [feature]/
        │       ├── entities/
        │       └── value_objects/
        │
        ├── api/
        │   └── [feature]/
        │       ├── commands/
        │       └── queries/
        │
        └── events/
            └── [feature]/
                ├── handlers/
                └── mappers/
```

## 3. Mobile

```plaintext
mobile/
├── lib/
│   ├── core/                           # Core functionality
│   │   ├── architecture/              # Architecture foundations
│   │   │   ├── base/
│   │   │   │   ├── usecase_base.dart  # Base usecase
│   │   │   │   ├── entity_base.dart   # Base entity
│   │   │   │   └── failure_base.dart  # Base failure
│   │   │   │
│   │   │   ├── bloc/                 # BLoC architecture
│   │   │   │   ├── base_bloc.dart    # Base BLoC
│   │   │   │   ├── base_event.dart   # Base event
│   │   │   │   └── base_state.dart   # Base state
│   │   │   │
│   │   │   └── repository/          # Repository architecture
│   │   │       ├── base_repository.dart
│   │   │       └── repository_exception.dart
│   │   │
│   │   ├── bloc/                    # BLoC utilities
│   │   │   ├── observers/          # BLoC observers
│   │   │   │   ├── app_bloc_observer.dart
│   │   │   │   └── error_bloc_observer.dart
│   │   │   │
│   │   │   ├── middleware/         # BLoC middleware
│   │   │   │   ├── logging_middleware.dart
│   │   │   │   └── error_middleware.dart
│   │   │   │
│   │   │   └── transformers/      # Stream transformers
│   │   │       ├── debounce_transformer.dart
│   │   │       └── throttle_transformer.dart
│   │   │
│   │   ├── config/                  # Configuration
│   │   │   ├── app/
│   │   │   │   ├── app_config.dart
│   │   │   │   ├── build_config.dart
│   │   │   │   └── environment/
│   │   │   │       ├── env.dart
│   │   │   │       ├── dev_env.dart
│   │   │   │       └── prod_env.dart
│   │   │   │
│   │   │   ├── theme/
│   │   │   │   ├── theme_config.dart
│   │   │   │   ├── themes/
│   │   │   │   │   ├── light_theme.dart
│   │   │   │   │   └── dark_theme.dart
│   │   │   │   │
│   │   │   │   └── styles/
│   │   │   │       ├── colors.dart
│   │   │   │       ├── typography.dart
│   │   │   │       └── dimensions.dart
│   │   │   │
│   │   │   └── routes/
│   │   │       ├── route_config.dart
│   │   │       └── route_guards.dart
│   │   │
│   │   ├── di/                      # Dependency injection
│   │   │   ├── providers/          # Riverpod providers
│   │   │   │   ├── core/          # Core providers
│   │   │   │   │   ├── network_providers.dart
│   │   │   │   │   └── storage_providers.dart
│   │   │   │   │
│   │   │   │   ├── feature/       # Feature providers
│   │   │   │   │   └── [feature]/
│   │   │   │   │       ├── repository_provider.dart
│   │   │   │   │       ├── usecase_provider.dart
│   │   │   │   │       └── bloc_provider.dart
│   │   │   │   │
│   │   │   │   └── state/         # State providers
│   │   │   │       ├── auth_state_provider.dart
│   │   │   │       └── app_state_provider.dart
│   │   │   │
│   │   │   └── injection/         # Get_it configuration
│   │   │       ├── injection.dart
│   │   │       └── injection.config.dart
│   │   │
│   │   ├── network/                # Network handling
│   │   │   ├── client/
│   │   │   │   ├── http_client.dart
│   │   │   │   └── api_client.dart
│   │   │   │
│   │   │   ├── interceptors/
│   │   │   │   ├── auth_interceptor.dart
│   │   │   │   ├── error_interceptor.dart
│   │   │   │   └── logging_interceptor.dart
│   │   │   │
│   │   │   ├── middleware/
│   │   │   │   ├── connectivity_middleware.dart
│   │   │   │   └── retry_middleware.dart
│   │   │   │
│   │   │   └── errors/
│   │   │       ├── network_error.dart
│   │   │       └── error_handler.dart
│   │   │
│   │   └── utils/                  # Utilities
│   │       ├── extensions/         # Extension methods
│   │       │   ├── context_extension.dart
│   │       │   ├── string_extension.dart
│   │       │   └── date_extension.dart
│   │       │
│   │       ├── validators/        # Input validation
│   │       │   ├── input_validator.dart
│   │       │   └── form_validator.dart
│   │       │
│   │       └── helpers/          # Helper utilities
│   │           ├── logger.dart
│   │           └── analytics.dart
│   │
│   ├── features/                   # Feature modules
│   │   └── [feature]/             # Each feature follows Clean Architecture
│   │       ├── domain/            # Domain layer
│   │       │   ├── entities/      # Business objects
│   │       │   │   ├── [entity].dart
│   │       │   │   └── [entity].freezed.dart
│   │       │   │
│   │       │   ├── value_objects/ # Value objects
│   │       │   │   └── [vo].dart
│   │       │   │
│   │       │   ├── repositories/  # Repository interfaces
│   │       │   │   └── i_[feature]_repository.dart
│   │       │   │
│   │       │   └── usecases/     # Business logic
│   │       │       ├── commands/  # Write operations
│   │       │       │   ├── create_[entity]_usecase.dart
│   │       │       │   └── update_[entity]_usecase.dart
│   │       │       │
│   │       │       └── queries/   # Read operations
│   │       │           ├── get_[entity]_usecase.dart
│   │       │           └── list_[entity]_usecase.dart
│   │       │
│   │       ├── data/             # Data layer
│   │       │   ├── models/       # Data models
│   │       │   │   ├── [entity]_model.dart
│   │       │   │   ├── [entity]_model.freezed.dart
│   │       │   │   └── [entity]_model.g.dart
│   │       │   │
│   │       │   ├── repositories/ # Repository implementations
│   │       │   │   └── [feature]_repository_impl.dart
│   │       │   │
│   │       │   ├── datasources/  # Data sources
│   │       │   │   ├── remote/
│   │       │   │   │   ├── i_[feature]_remote_source.dart
│   │       │   │   │   └── [feature]_remote_source_impl.dart
│   │       │   │   │
│   │       │   │   └── local/
│   │       │   │       ├── i_[feature]_local_source.dart
│   │       │   │       └── [feature]_local_source_impl.dart
│   │       │   │
│   │       │   └── mappers/      # Data mappers
│   │       │       └── [entity]_mapper.dart
│   │       │
│   │       └── presentation/     # Presentation layer
│   │           ├── bloc/         # BLoC pattern implementation
│   │           │   ├── [feature]_bloc.dart
│   │           │   ├── [feature]_event.dart
│   │           │   └── [feature]_state.dart
│   │           │
│   │           ├── pages/        # Feature pages
│   │           │   ├── [feature]_page.dart
│   │           │   └── widgets/  # Page-specific widgets
│   │           │       └── [widget].dart
│   │           │
│   │           └── widgets/      # Shared feature widgets
│   │               └── [widget].dart
│   │
│   └── shared/                   # Shared components
│       ├── widgets/             # Common widgets
│       │   ├── buttons/
│       │   │   ├── primary_button.dart
│       │   │   └── secondary_button.dart
│       │   │
│       │   ├── inputs/
│       │   │   ├── text_input.dart
│       │   │   └── search_input.dart
│       │   │
│       │   └── feedback/
│       │       ├── loading_indicator.dart
│       │       └── error_view.dart
│       │
│       └── behaviors/          # Shared behaviors
│           ├── scroll_behavior.dart
│           └── tap_behavior.dart
```

## 4. Backend

```plaintext
backend/
├── src/
│   ├── domain/                    # Domain Layer
│   │   ├── aggregates/           # DDD Aggregates
│   │   │   └── [aggregate_name]/
│   │   │       ├── entities/     # Aggregate entities
│   │   │       │   ├── [entity].py
│   │   │       │   └── [entity]_validator.py
│   │   │       │
│   │   │       ├── value_objects/  # Value objects
│   │   │       │   ├── [vo].py
│   │   │       │   └── [vo]_validator.py
│   │   │       │
│   │   │       ├── specifications/ # Business rules
│   │   │       │   └── [spec_name]_specification.py
│   │   │       │
│   │   │       └── services/      # Domain services
│   │   │           └── [service_name]_service.py
│   │   │
│   │   ├── events/               # Domain events
│   │   │   ├── base/
│   │   │   │   ├── domain_event.py
│   │   │   │   └── event_handler.py
│   │   │   │
│   │   │   └── [aggregate]/
│   │   │       ├── events/
│   │   │       │   ├── [event]_event.py
│   │   │       │   └── [event]_payload.py
│   │   │       │
│   │   │       └── handlers/
│   │   │           └── [event]_handler.py
│   │   │
│   │   ├── exceptions/          # Domain exceptions
│   │   │   ├── base_exception.py
│   │   │   ├── validation_exception.py
│   │   │   └── business_exception.py
│   │   │
│   │   └── ports/              # Ports (interfaces)
│   │       ├── repositories/   # Repository interfaces
│   │       │   └── i_[aggregate]_repository.py
│   │       │
│   │       └── services/      # Service interfaces
│   │           └── i_[service]_port.py
│   │
│   ├── application/           # Application Layer
│   │   ├── cqrs/             # CQRS pattern
│   │   │   ├── commands/     # Write operations
│   │   │   │   └── [aggregate]/
│   │   │   │       ├── commands/
│   │   │   │       │   ├── create_[entity]_command.py
│   │   │   │       │   └── update_[entity]_command.py
│   │   │   │       │
│   │   │   │       └── handlers/
│   │   │   │           ├── create_[entity]_handler.py
│   │   │   │           └── update_[entity]_handler.py
│   │   │   │
│   │   │   └── queries/     # Read operations
│   │   │       └── [aggregate]/
│   │   │           ├── queries/
│   │   │           │   ├── get_[entity]_query.py
│   │   │           │   └── list_[entity]_query.py
│   │   │           │
│   │   │           ├── handlers/
│   │   │           │   ├── get_[entity]_handler.py
│   │   │           │   └── list_[entity]_handler.py
│   │   │           │
│   │   │           └── projections/
│   │   │               └── [entity]_projection.py
│   │   │
│   │   ├── event_sourcing/   # Event sourcing
│   │   │   ├── store/
│   │   │   │   ├── event_store.py
│   │   │   │   └── event_stream.py
│   │   │   │
│   │   │   ├── snapshots/
│   │   │   │   ├── snapshot_store.py
│   │   │   │   └── snapshot_strategy.py
│   │   │   │
│   │   │   └── projection/
│   │   │       ├── projection_manager.py
│   │   │       └── event_processor.py
│   │   │
│   │   ├── sagas/           # Saga pattern
│   │   │   ├── orchestration/
│   │   │   │   ├── saga_manager.py
│   │   │   │   └── [process]/
│   │   │   │       ├── saga_definition.py
│   │   │   │       └── saga_steps.py
│   │   │   │
│   │   │   └── compensation/
│   │   │       ├── compensation_manager.py
│   │   │       └── [process]/
│   │   │           ├── compensating_actions.py
│   │   │           └── recovery_policy.py
│   │   │
│   │   └── services/        # Application services
│   │       └── [service]/
│   │           ├── service.py
│   │           ├── mapper.py
│   │           └── validator.py
│   │
│   ├── infrastructure/       # Infrastructure Layer
│   │   ├── persistence/     # Data persistence
│   │   │   ├── models/     # ORM models
│   │   │   │   └── [aggregate]/
│   │   │   │       ├── [entity]_model.py
│   │   │   │       └── relationships.py
│   │   │   │
│   │   │   ├── repositories/
│   │   │   │   └── [aggregate]/
│   │   │   │       ├── repository.py
│   │   │   │       └── query_sets.py
│   │   │   │
│   │   │   └── migrations/
│   │   │       └── versions/
│   │   │
│   │   ├── messaging/      # Message handling
│   │   │   ├── kafka/     # Kafka implementation
│   │   │   │   ├── producers/
│   │   │   │   │   └── [event]_producer.py
│   │   │   │   │
│   │   │   │   └── consumers/
│   │   │   │       └── [event]_consumer.py
│   │   │   │
│   │   │   ├── rabbitmq/  # RabbitMQ implementation
│   │   │   │   ├── producers/
│   │   │   │   └── consumers/
│   │   │   │
│   │   │   └── event_bus/
│   │   │       ├── event_dispatcher.py
│   │   │       └── event_subscriber.py
│   │   │
│   │   ├── cache/         # Caching
│   │   │   ├── redis/
│   │   │   │   ├── client.py
│   │   │   │   └── serializer.py
│   │   │   │
│   │   │   └── memory/
│   │   │       └── cache.py
│   │   │
│   │   └── external/      # External services
│   │       └── [service_name]/
│   │           ├── client.py
│   │           ├── config.py
│   │           └── dto/
│   │               ├── requests.py
│   │               └── responses.py
│   │
│   ├── ports/             # Ports (adapters)
│   │   ├── http/         # HTTP endpoints
│   │   │   └── v1/
│   │   │       ├── [aggregate]/
│   │   │       │   ├── routes.py
│   │   │       │   ├── schemas.py
│   │   │       │   └── controllers.py
│   │   │       │
│   │   │       └── middleware/
│   │   │           ├── auth.py
│   │   │           └── logging.py
│   │   │
│   │   ├── grpc/        # gRPC endpoints
│   │   │   └── [service]/
│   │   │       ├── service.py
│   │   │       └── handlers.py
│   │   │
│   │   └── websocket/   # WebSocket endpoints
│   │       └── [feature]/
│   │           ├── handler.py
│   │           └── manager.py
│   │
│   └── core/            # Core module
│       ├── config/     # Configuration
│       │   ├── settings.py
│       │   └── environment.py
│       │
│       ├── logging/    # Logging
│       │   ├── logger.py
│       │   └── handlers.py
│       │
│       └── security/   # Security
│           ├── authentication.py
│           └── authorization.py
```

## 5. DevOps

```plaintext
infrastructure/                    # Infrastructure and DevOps
├── mesh/                         # Service Mesh
│   ├── gateway/                 # API Gateway
│   │   ├── routes/             # Route definitions
│   │   │   ├── [service]/
│   │   │   │   ├── routes.yaml
│   │   │   │   └── rewrite.yaml
│   │   │   │
│   │   │   └── global/
│   │   │       ├── cors.yaml
│   │   │       └── security.yaml
│   │   │
│   │   ├── policies/          # Gateway policies
│   │   │   ├── rate_limiting/
│   │   │   │   ├── [service]_limits.yaml
│   │   │   │   └── global_limits.yaml
│   │   │   │
│   │   │   ├── circuit_breaker/
│   │   │   │   ├── [service]_breaker.yaml
│   │   │   │   └── global_breaker.yaml
│   │   │   │
│   │   │   └── security/
│   │   │       ├── auth_policies.yaml
│   │   │       └── jwt_config.yaml
│   │   │
│   │   └── middleware/        # Gateway middleware
│   │       ├── auth/
│   │       │   ├── jwt_validator.yaml
│   │       │   └── oauth_config.yaml
│   │       │
│   │       ├── logging/
│   │       │   ├── access_log.yaml
│   │       │   └── error_log.yaml
│   │       │
│   │       └── metrics/
│   │           └── prometheus_metrics.yaml
│   │
│   ├── service_mesh/          # Service Mesh components
│   │   ├── istio/            # Istio configuration
│   │   │   ├── config/
│   │   │   │   ├── mesh.yaml
│   │   │   │   └── profiles/
│   │   │   │       ├── default.yaml
│   │   │   │       └── prod.yaml
│   │   │   │
│   │   │   ├── security/
│   │   │   │   ├── auth_policies.yaml
│   │   │   │   └── mtls_config.yaml
│   │   │   │
│   │   │   └── traffic/
│   │   │       ├── circuit_breaker.yaml
│   │   │       └── load_balancer.yaml
│   │   │
│   │   └── consul/           # Consul configuration
│   │       ├── config/
│   │       │   ├── server.json
│   │       │   └── client.json
│   │       │
│   │       └── services/
│   │           └── [service].json
│   │
│   └── networking/           # Network configuration
│       ├── ingress/
│       │   ├── rules/
│       │   │   └── [service]_ingress.yaml
│       │   │
│       │   └── tls/
│       │       └── certificates.yaml
│       │
│       └── service_discovery/
│           ├── dns_config.yaml
│           └── endpoints.yaml
│
├── kubernetes/                # Kubernetes configurations
│   ├── base/                # Base configurations
│   │   ├── namespaces/
│   │   │   ├── dev.yaml
│   │   │   └── prod.yaml
│   │   │
│   │   ├── workloads/      # Workload definitions
│   │   │   ├── deployments/
│   │   │   │   └── [service]/
│   │   │   │       ├── deployment.yaml
│   │   │   │       └── hpa.yaml
│   │   │   │
│   │   │   └── statefulsets/
│   │   │       └── [service]/
│   │   │           └── statefulset.yaml
│   │   │
│   │   ├── networking/     # Network resources
│   │   │   ├── services/
│   │   │   │   └── [service].yaml
│   │   │   │
│   │   │   └── ingress/
│   │   │       └── [service].yaml
│   │   │
│   │   └── storage/       # Storage resources
│   │       ├── persistent_volumes/
│   │       │   └── [volume].yaml
│   │       │
│   │       └── storage_classes/
│   │           └── [class].yaml
│   │
│   └── overlays/          # Environment overlays
│       ├── development/
│       │   ├── kustomization.yaml
│       │   └── patches/
│       │       └── [service]/
│       │           └── deployment_patch.yaml
│       │
│       └── production/
│           ├── kustomization.yaml
│           └── patches/
│               └── [service]/
│                   └── deployment_patch.yaml
│
├── monitoring/               # Monitoring and observability
│   ├── prometheus/         # Prometheus configuration
│   │   ├── rules/
│   │   │   ├── recording_rules.yaml
│   │   │   └── alerting_rules.yaml
│   │   │
│   │   ├── alerts/
│   │   │   └── [service]/
│   │   │       ├── availability.yaml
│   │   │       └── performance.yaml
│   │   │
│   │   └── scrape_configs/
│   │       └── [service].yaml
│   │
│   ├── grafana/            # Grafana configuration
│   │   ├── dashboards/
│   │   │   ├── overview/
│   │   │   │   └── system_overview.json
│   │   │   │
│   │   │   └── [service]/
│   │   │       ├── performance.json
│   │   │       └── errors.json
│   │   │
│   │   └── datasources/
│   │       └── prometheus.yaml
│   │
│   ├── logging/           # Logging configuration
│   │   ├── elasticsearch/
│   │   │   ├── config.yaml
│   │   │   └── templates/
│   │   │       └── [index_template].json
│   │   │
│   │   ├── fluentd/
│   │   │   └── config/
│   │   │       └── fluent.conf
│   │   │
│   │   └── kibana/
│   │       └── dashboards/
│   │           └── [dashboard].json
│   │
│   └── tracing/           # Distributed tracing
│       ├── jaeger/
│       │   └── config.yaml
│       │
│       └── opentelemetry/
│           └── config.yaml
│
└── ci_cd/                  # CI/CD configuration
    ├── pipelines/
    │   ├── backend/
    │   │   ├── build.yaml
    │   │   ├── test.yaml
    │   │   └── deploy.yaml
    │   │
    │   └── mobile/
    │       ├── build.yaml
    │       ├── test.yaml
    │       └── deploy.yaml
    │
    ├── scripts/
    │   ├── deployment/
    │   │   ├── deploy_service.sh
    │   │   └── rollback_service.sh
    │   │
    │   └── monitoring/
    │       ├── health_check.sh
    │       └── alerts_check.sh
    │
    └── templates/
        ├── dockerfiles/
        │   ├── backend.dockerfile
        │   └── mobile.dockerfile
        │
        └── helm/
            └── [service]/
                ├── Chart.yaml
                ├── values.yaml
                └── templates/
```

```plaintext
tools/                              # Development tools and utilities
├── generators/                     # Code generation tools
│   ├── api/                       # API code generators
│   │   ├── templates/            # Code templates
│   │   │   ├── flutter/
│   │   │   │   ├── api_client.dart.jinja
│   │   │   │   ├── model.dart.jinja
│   │   │   │   └── repository.dart.jinja
│   │   │   │
│   │   │   └── python/
│   │   │       ├── endpoint.py.jinja
│   │   │       ├── model.py.jinja
│   │   │       └── repository.py.jinja
│   │   │
│   │   ├── schemas/             # API schema definitions
│   │   │   ├── openapi.yaml
│   │   │   └── graphql.graphql
│   │   │
│   │   └── scripts/
│   │       ├── generate_client.py
│   │       ├── generate_models.py
│   │       └── generate_docs.py
│   │
│   ├── proto/                    # Protocol buffer generators
│   │   ├── templates/
│   │   │   ├── service.proto.jinja
│   │   │   └── message.proto.jinja
│   │   │
│   │   └── scripts/
│   │       ├── generate_proto.sh
│   │       └── compile_proto.sh
│   │
│   └── testing/                  # Test generators
│       ├── templates/
│       │   ├── flutter/
│       │   │   ├── bloc_test.dart.jinja
│       │   │   └── widget_test.dart.jinja
│       │   │
│       │   └── python/
│       │       ├── unit_test.py.jinja
│       │       └── integration_test.py.jinja
│       │
│       └── scripts/
│           ├── generate_tests.py
│           └── generate_mocks.py
│
├── scripts/                        # Development scripts
│   ├── setup/                     # Environment setup
│   │   ├── dev/
│   │   │   ├── setup_dev_env.sh
│   │   │   ├── install_dependencies.sh
│   │   │   └── configure_ide.sh
│   │   │
│   │   ├── ci/
│   │   │   ├── setup_ci_env.sh
│   │   │   └── configure_runners.sh
│   │   │
│   │   └── cloud/
│   │       ├── setup_aws.sh
│   │       ├── setup_gcp.sh
│   │       └── setup_azure.sh
│   │
│   ├── database/                  # Database utilities
│   │   ├── migration/
│   │   │   ├── create_migration.py
│   │   │   ├── apply_migration.py
│   │   │   └── rollback_migration.py
│   │   │
│   │   └── seeding/
│   │       ├── seed_data.py
│   │       └── clear_data.py
│   │
│   ├── deployment/                # Deployment utilities
│   │   ├── kubernetes/
│   │   │   ├── deploy_service.sh
│   │   │   └── update_service.sh
│   │   │
│   │   ├── docker/
│   │   │   ├── build_images.sh
│   │   │   └── push_images.sh
│   │   │
│   │   └── monitoring/
│   │       ├── setup_monitoring.sh
│   │       └── configure_alerts.sh
│   │
│   └── testing/                   # Testing utilities
│       ├── unit/
│       │   ├── run_flutter_tests.sh
│       │   └── run_python_tests.sh
│       │
│       ├── integration/
│       │   ├── setup_test_env.sh
│       │   └── run_integration_tests.sh
│       │
│       └── performance/
│           ├── run_load_tests.sh
│           └── analyze_performance.sh
│
├── analysis/                       # Code analysis tools
│   ├── linting/                  # Linting configurations
│   │   ├── flutter/
│   │   │   ├── analysis_options.yaml
│   │   │   └── lint_rules.yaml
│   │   │
│   │   └── python/
│   │       ├── pylintrc
│   │       └── flake8.cfg
│   │
│   ├── security/                 # Security analysis
│   │   ├── dependency_check.sh
│   │   └── code_scanning.sh
│   │
│   └── metrics/                  # Code metrics
│       ├── complexity_check.py
│       └── coverage_report.py
│
├── documentation/                  # Documentation tools
│   ├── api/                      # API documentation
│   │   ├── generators/
│   │   │   ├── openapi_gen.py
│   │   │   └── graphql_gen.py
│   │   │
│   │   └── templates/
│   │       ├── endpoint.md.jinja
│   │       └── schema.md.jinja
│   │
│   ├── architecture/             # Architecture documentation
│   │   ├── diagrams/
│   │   │   ├── generate_c4.py
│   │   │   └── generate_sequence.py
│   │   │
│   │   └── templates/
│   │       ├── component.md.jinja
│   │       └── decision_record.md.jinja
│   │
│   └── release/                  # Release documentation
│       ├── changelog_generator.py
│       └── release_notes_template.md
│
└── hooks/                         # Git hooks
    ├── pre-commit/               # Pre-commit hooks
    │   ├── lint_check.sh
    │   ├── format_check.sh
    │   └── test_check.sh
    │
    ├── pre-push/                # Pre-push hooks
    │   ├── integration_test.sh
    │   └── coverage_check.sh
    │
    └── commit-msg/              # Commit message hooks
        └── commit_check.sh
```
