project_root/
├── shared/                          # Single source of truth for all services
│   ├── models/                      # Core domain models
│   │   └── [feature]/              # Feature-specific models
│   │       ├── models/             # Core models
│   │       │   ├── [model].model.yaml        # Schema definition
│   │       │   ├── [model].model.dart        # Flutter model
│   │       │   └── [model].model.py          # Python model
│   │       │
│   │       ├── value_objects/      # Value objects
│   │       │   ├── [vo].vo.yaml             # VO definition
│   │       │   ├── [vo].vo.dart             # Flutter VO
│   │       │   └── [vo].vo.py               # Python VO
│   │       │
│   │       └── enums/             # Enumerations
│   │           ├── [enum].enum.yaml         # Enum definition
│   │           ├── [enum].enum.dart         # Flutter enum
│   │           └── [enum].enum.py           # Python enum
│   │
│   ├── api/                        # API contracts
│   │   ├── schemas/               # Base schemas
│   │   │   ├── base_request.yaml         # Base request
│   │   │   ├── base_response.yaml        # Base response
│   │   │   └── error_response.yaml       # Error schema
│   │   │
│   │   ├── requests/              # Request definitions
│   │   │   └── [feature]/
│   │   │       ├── commands/             # Command requests
│   │   │       │   ├── [command].request.yaml
│   │   │       │   ├── [command].request.dart
│   │   │       │   └── [command].request.py
│   │   │       └── queries/              # Query requests
│   │   │           ├── [query].request.yaml
│   │   │           ├── [query].request.dart
│   │   │           └── [query].request.py
│   │   │
│   │   ├── responses/             # Response definitions
│   │   │   └── [feature]/
│   │   │       ├── commands/             # Command responses
│   │   │       │   ├── [command].response.yaml
│   │   │       │   ├── [command].response.dart
│   │   │       │   └── [command].response.py
│   │   │       └── queries/              # Query responses
│   │   │           ├── [query].response.yaml
│   │   │           ├── [query].response.dart
│   │   │           └── [query].response.py
│   │   │
│   │   └── validations/           # Validation rules
│   │       └── [feature]/
│   │           ├── commands/
│   │           │   └── [command].validation.yaml
│   │           └── queries/
│   │               └── [query].validation.yaml
│   │
│   ├── events/                     # Event-driven architecture
│   │   ├── base/                  # Base event definitions
│   │   │   ├── base_event.yaml           # Base event schema
│   │   │   ├── base_event.dart           # Flutter base event
│   │   │   └── base_event.py             # Python base event
│   │   │
│   │   └── [feature]/            # Feature events
│   │       ├── commands/          # Command events
│   │       │   ├── [command].event.yaml
│   │       │   ├── [command].event.dart
│   │       │   └── [command].event.py
│   │       │
│   │       └── domain/            # Domain events
│   │           ├── [event].event.yaml
│   │           ├── [event].event.dart
│   │           └── [event].event.py
│   │
│   ├── commands/                   # CQRS - Commands
│   │   ├── base/                 # Base command definitions
│   │   │   ├── base_command.yaml        # Base command schema
│   │   │   └── base_handler.yaml        # Base handler schema
│   │   │
│   │   └── [feature]/           # Feature commands
│   │       ├── definitions/
│   │       │   ├── [command].command.yaml
│   │       │   └── [command].handler.yaml
│   │       │
│   │       └── validations/
│   │           └── [command].validation.yaml
│   │
│   └── queries/                    # CQRS - Queries
│       ├── base/                 # Base query definitions
│       │   ├── base_query.yaml          # Base query schema
│       │   └── base_handler.yaml        # Base handler schema
│       │
│       └── [feature]/           # Feature queries
│           ├── definitions/
│           │   ├── [query].query.yaml
│           │   └── [query].handler.yaml
│           │
│           └── validations/
│               └── [query].validation.yaml
├── mobile/                         # Flutter Clean Architecture + MVVM
│   ├── lib/
│   │   ├── core/                  # Core Layer
│   │   │   ├── base/             # Base implementations
│   │   │   │   ├── presentation/ # Base presentation components
│   │   │   │   │   ├── base_view.dart          # Base view widget
│   │   │   │   │   ├── base_view.freezed.dart  # Generated code
│   │   │   │   │   ├── base_viewmodel.dart     # Base viewmodel
│   │   │   │   │   ├── base_state.dart         # Base state
│   │   │   │   │   └── view_state.dart         # View state enum
│   │   │   │   │
│   │   │   │   ├── domain/      # Base domain components
│   │   │   │   │   ├── base_entity.dart        # Base entity
│   │   │   │   │   ├── base_value_object.dart  # Base value object
│   │   │   │   │   └── base_failure.dart       # Base failure
│   │   │   │   │
│   │   │   │   ├── data/       # Base data components
│   │   │   │   │   ├── base_model.dart         # Base data model
│   │   │   │   │   ├── base_repository.dart    # Base repository
│   │   │   │   │   └── base_datasource.dart    # Base data source
│   │   │   │   │
│   │   │   │   └── usecases/   # Base use cases
│   │   │   │       ├── base_usecase.dart       # Base use case
│   │   │   │       ├── future_usecase.dart     # Future use case
│   │   │   │       └── stream_usecase.dart     # Stream use case
│   │   │   │
│   │   │   ├── di/            # Dependency injection
│   │   │   │   ├── modules/    # DI modules
│   │   │   │   │   ├── api_module.dart        # API dependencies
│   │   │   │   │   ├── storage_module.dart    # Storage dependencies
│   │   │   │   │   └── service_module.dart    # Service dependencies
│   │   │   │   ├── injection.dart             # DI setup
│   │   │   │   └── injection.config.dart      # Generated DI
│   │   │   │
│   │   │   ├── network/       # Network handling
│   │   │   │   ├── client/    # HTTP client
│   │   │   │   │   ├── api_client.dart        # API client
│   │   │   │   │   ├── api_config.dart        # Client config
│   │   │   │   │   └── endpoints.dart         # API endpoints
│   │   │   │   │
│   │   │   │   ├── interceptors/  # Request interceptors
│   │   │   │   │   ├── auth_interceptor.dart
│   │   │   │   │   ├── error_interceptor.dart
│   │   │   │   │   ├── logging_interceptor.dart
│   │   │   │   │   └── retry_interceptor.dart
│   │   │   │   │
│   │   │   │   └── errors/    # Network errors
│   │   │   │       ├── network_error.dart     # Error types
│   │   │   │       ├── error_handler.dart     # Error handling
│   │   │   │       └── error_mapper.dart      # Error mapping
│   │   │   │
│   │   │   ├── storage/      # Local storage
│   │   │   │   ├── secure/   # Secure storage
│   │   │   │   │   ├── secure_storage.dart    # Encrypted storage
│   │   │   │   │   └── key_storage.dart       # Key management
│   │   │   │   │
│   │   │   │   ├── cache/    # Cache storage
│   │   │   │   │   ├── cache_storage.dart     # Cache implementation
│   │   │   │   │   └── cache_policy.dart      # Caching policy
│   │   │   │   │
│   │   │   │   └── local/    # Local storage
│   │   │   │       ├── local_storage.dart     # Local storage
│   │   │   │       └── storage_keys.dart      # Storage keys
│   │   │   │
│   │   │   ├── analytics/    # Analytics & monitoring
│   │   │   │   ├── analytics_service.dart     # Analytics interface
│   │   │   │   ├── firebase_analytics.dart    # Firebase implementation
│   │   │   │   └── crash_reporting.dart       # Crash reporting
│   │   │   │
│   │   │   ├── logging/      # Logging
│   │   │   │   ├── logger.dart               # Logger setup
│   │   │   │   └── log_level.dart           # Log levels
│   │   │   │
│   │   │   └── utils/        # Utilities
│   │   │       ├── extensions/  # Extensions
│   │   │       │   ├── context_extension.dart
│   │   │       │   ├── string_extension.dart
│   │   │       │   ├── datetime_extension.dart
│   │   │       │   └── iterable_extension.dart
│   │   │       │
│   │   │       ├── validators/ # Validators
│   │   │       │   ├── email_validator.dart
│   │   │       │   ├── password_validator.dart
│   │   │       │   └── input_validator.dart
│   │   │       │
│   │   │       └── helpers/    # Helper functions
│   │   │           ├── date_helper.dart
│   │   │           ├── string_helper.dart
│   │   │           └── number_helper.dart
│   │   │
│   │   ├── features/              # Feature modules
│   │   │   └── [feature]/        # Each feature following Clean Architecture
│   │   │       ├── data/         # Data Layer
│   │   │       │   ├── datasources/
│   │   │       │   │   ├── remote/
│   │   │       │   │   │   ├── [feature]_remote_source.dart      # Remote data source
│   │   │       │   │   │   ├── [feature]_remote_source.g.dart    # Generated code
│   │   │       │   │   │   ├── dtos/                            # DTOs for API
│   │   │       │   │   │   │   ├── request/
│   │   │       │   │   │   │   │   └── [dto]_request.dart       # Request DTOs
│   │   │       │   │   │   │   └── response/
│   │   │       │   │   │   │       └── [dto]_response.dart      # Response DTOs
│   │   │       │   │   │   └── mappers/
│   │   │       │   │   │       └── [dto]_mapper.dart            # DTO mappers
│   │   │       │   │   │
│   │   │       │   │   └── local/
│   │   │       │   │       ├── [feature]_local_source.dart       # Local data source
│   │   │       │   │       ├── [feature]_local_source.g.dart     # Generated code
│   │   │       │   │       ├── daos/                            # Database objects
│   │   │       │   │       │   └── [dao].dart                   # Data Access Objects
│   │   │       │   │       └── mappers/
│   │   │       │   │           └── [dao]_mapper.dart            # DAO mappers
│   │   │       │   │
│   │   │       │   ├── models/              # Data models
│   │   │       │   │   ├── [model].dart                         # Data model
│   │   │       │   │   ├── [model].freezed.dart                 # Immutable model
│   │   │       │   │   └── [model].g.dart                       # JSON serialization
│   │   │       │   │
│   │   │       │   └── repositories/        # Repository implementations
│   │   │       │       ├── [feature]_repository_impl.dart       # Repository impl
│   │   │       │       ├── mappers/
│   │   │       │       │   └── [entity]_mapper.dart             # Entity mappers
│   │   │       │       └── cache/
│   │   │       │           └── [feature]_cache_policy.dart      # Cache policy
│   │   │       │
│   │   │       ├── domain/                 # Domain Layer
│   │   │       │   ├── entities/           # Business entities
│   │   │       │   │   ├── [entity].dart                        # Entity
│   │   │       │   │   └── [entity].freezed.dart                # Immutable entity
│   │   │       │   │
│   │   │       │   ├── value_objects/      # Value objects
│   │   │       │   │   └── [vo].dart                           # Value object
│   │   │       │   │
│   │   │       │   ├── repositories/       # Repository interfaces
│   │   │       │   │   └── [feature]_repository.dart            # Repository contract
│   │   │       │   │
│   │   │       │   ├── usecases/          # Business use cases
│   │   │       │   │   ├── commands/      # Command use cases
│   │   │       │   │   │   ├── create_[feature].dart           # Create
│   │   │       │   │   │   ├── update_[feature].dart           # Update
│   │   │       │   │   │   └── delete_[feature].dart           # Delete
│   │   │       │   │   │
│   │   │       │   │   └── queries/       # Query use cases
│   │   │       │   │       ├── get_[feature].dart              # Get
│   │   │       │   │       └── list_[features].dart            # List
│   │   │       │   │
│   │   │       │   └── failures/          # Domain failures
│   │   │       │       └── [feature]_failure.dart               # Feature failures
│   │   │       │
│   │   │       └── presentation/          # Presentation Layer (MVVM)
│   │   │           ├── viewmodels/        # ViewModels
│   │   │           │   ├── [feature]_viewmodel.dart             # ViewModel
│   │   │           │   ├── [feature]_state.dart                 # State
│   │   │           │   ├── [feature]_state.freezed.dart         # Generated state
│   │   │           │   └── mappers/
│   │   │           │       └── [view]_mapper.dart               # View mappers
│   │   │           │
│   │   │           ├── views/            # Views
│   │   │           │   ├── pages/        # Pages
│   │   │           │   │   ├── [feature]_page.dart             # Main page
│   │   │           │   │   └── subpages/
│   │   │           │   │       └── [subpage].dart              # Sub pages
│   │   │           │   │
│   │   │           │   └── dialogs/      # Dialogs
│   │   │           │       └── [dialog].dart                   # Feature dialogs
│   │   │           │
│   │   │           └── widgets/         # Feature-specific widgets
│   │   │               ├── items/       # List items
│   │   │               │   └── [item].dart                     # Item widgets
│   │   │               ├── forms/       # Form widgets
│   │   │               │   └── [form].dart                     # Form widgets
│   │   │               └── common/      # Common widgets
│   │   │                   └── [widget].dart                   # Reusable widgets
│   │   │
│   │   ├── shared/                  # Shared components
│   │   │   ├── widgets/            # Reusable widgets
│   │   │   │   ├── buttons/        # Button components
│   │   │   │   │   ├── primary_button.dart
│   │   │   │   │   ├── secondary_button.dart
│   │   │   │   │   ├── icon_button.dart
│   │   │   │   │   └── loading_button.dart
│   │   │   │   │
│   │   │   │   ├── inputs/         # Input components
│   │   │   │   │   ├── text_input.dart
│   │   │   │   │   ├── password_input.dart
│   │   │   │   │   ├── search_input.dart
│   │   │   │   │   └── date_input.dart
│   │   │   │   │
│   │   │   │   ├── cards/          # Card components
│   │   │   │   │   ├── base_card.dart
│   │   │   │   │   └── info_card.dart
│   │   │   │   │
│   │   │   │   ├── dialogs/        # Dialog components
│   │   │   │   │   ├── alert_dialog.dart
│   │   │   │   │   ├── confirm_dialog.dart
│   │   │   │   │   └── loading_dialog.dart
│   │   │   │   │
│   │   │   │   └── indicators/     # Loading indicators
│   │   │   │       ├── loading_indicator.dart
│   │   │   │       └── error_indicator.dart
│   │   │   │
│   │   │   ├── styles/            # Shared styles
│   │   │   │   ├── colors.dart
│   │   │   │   ├── typography.dart
│   │   │   │   ├── dimensions.dart
│   │   │   │   └── theme.dart
│   │   │   │
│   │   │   └── animations/        # Shared animations
│   │   │       ├── fade_animation.dart
│   │   │       ├── slide_animation.dart
│   │   │       └── scale_animation.dart
│   │   │
│   │   └── l10n/                  # Localization
│   │       ├── app_localizations.dart
│   │       ├── app_en.arb
│   │       └── app_es.arb
│   │
│   ├── test/                      # Tests
│   │   ├── core/                 # Core tests
│   │   │   ├── network/
│   │   │   │   ├── api_client_test.dart
│   │   │   │   └── interceptors/
│   │   │   │       ├── auth_interceptor_test.dart
│   │   │   │       └── error_interceptor_test.dart
│   │   │   │
│   │   │   ├── storage/
│   │   │   │   ├── secure_storage_test.dart
│   │   │   │   └── cache_storage_test.dart
│   │   │   │
│   │   │   └── utils/
│   │   │       └── validators/
│   │   │           └── input_validator_test.dart
│   │   │
│   │   ├── features/             # Feature tests
│   │   │   └── [feature]/
│   │   │       ├── data/         # Data layer tests
│   │   │       │   ├── datasources/
│   │   │       │   │   ├── remote/
│   │   │       │   │   │   ├── remote_source_test.dart
│   │   │       │   │   │   └── mappers/
│   │   │       │   │   │       └── dto_mapper_test.dart
│   │   │       │   │   │
│   │   │       │   │   └── local/
│   │   │       │   │       ├── local_source_test.dart
│   │   │       │   │       └── mappers/
│   │   │       │   │           └── dao_mapper_test.dart
│   │   │       │   │
│   │   │       │   ├── models/
│   │   │       │   │   └── model_test.dart
│   │   │       │   │
│   │   │       │   └── repositories/
│   │   │       │       └── repository_impl_test.dart
│   │   │       │
│   │   │       ├── domain/       # Domain layer tests
│   │   │       │   ├── entities/
│   │   │       │   │   └── entity_test.dart
│   │   │       │   │
│   │   │       │   └── usecases/
│   │   │       │       ├── commands/
│   │   │       │       │   ├── create_test.dart
│   │   │       │       │   └── update_test.dart
│   │   │       │       └── queries/
│   │   │       │           ├── get_test.dart
│   │   │       │           └── list_test.dart
│   │   │       │
│   │   │       └── presentation/ # Presentation layer tests
│   │   │           ├── viewmodels/
│   │   │           │   └── viewmodel_test.dart
│   │   │           │
│   │   │           └── views/
│   │   │               └── view_test.dart
│   │   │
│   │   ├── shared/              # Shared component tests
│   │   │   └── widgets/
│   │   │       ├── buttons/
│   │   │       │   └── button_test.dart
│   │   │       └── inputs/
│   │   │           └── input_test.dart
│   │   │
│   │   └── helpers/             # Test helpers
│   │       ├── test_helpers.dart
│   │       ├── mock_helpers.dart
│   │       └── fake_data.dart
│   │
│   ├── integration_test/         # Integration tests
│   │   └── app_test.dart
│   │
│   ├── ios/                     # iOS specific
│   │   ├── Runner/
│   │   │   ├── AppDelegate.swift
│   │   │   └── Info.plist
│   │   └── Runner.xcodeproj/
│   │
│   ├── android/                 # Android specific
│   │   ├── app/
│   │   │   ├── src/
│   │   │   │   └── main/
│   │   │   └── build.gradle
│   │   └── build.gradle
│   │
│   ├── assets/                  # Assets
│   │   ├── images/
│   │   ├── fonts/
│   │   └── icons/
│   │
│   ├── analysis_options.yaml    # Dart analysis options
│   ├── pubspec.yaml            # Dependencies
│   └── README.md              # Mobile documentation
│
├── backend/                      # FastAPI Microservices
│   ├── core_service/            # Core/Common service
│   │   ├── src/
│   │   │   ├── base/           # Base implementations
│   │   │   │   ├── commands/   # CQRS Command base
│   │   │   │   │   ├── base_command.py          # Base command class
│   │   │   │   │   ├── base_handler.py          # Base handler class
│   │   │   │   │   ├── command_bus.py           # Command dispatcher
│   │   │   │   │   └── command_result.py        # Command result
│   │   │   │   │
│   │   │   │   ├── queries/    # CQRS Query base
│   │   │   │   │   ├── base_query.py            # Base query class
│   │   │   │   │   ├── base_handler.py          # Base handler class
│   │   │   │   │   ├── query_bus.py             # Query dispatcher
│   │   │   │   │   └── query_result.py          # Query result
│   │   │   │   │
│   │   │   │   ├── events/     # Event base
│   │   │   │   │   ├── base_event.py            # Base event class
│   │   │   │   │   ├── event_bus.py             # Event dispatcher
│   │   │   │   │   ├── event_handler.py         # Event handler
│   │   │   │   │   └── event_store.py           # Event store
│   │   │   │   │
│   │   │   │   ├── models/     # Base models
│   │   │   │   │   ├── base_model.py            # Base model class
│   │   │   │   │   ├── base_entity.py           # Base entity class
│   │   │   │   │   └── base_vo.py               # Base value object
│   │   │   │   │
│   │   │   │   ├── repository/ # Base repository
│   │   │   │   │   ├── base_repository.py       # Base repo interface
│   │   │   │   │   ├── base_crud.py            # CRUD operations
│   │   │   │   │   └── unit_of_work.py         # Unit of Work pattern
│   │   │   │   │
│   │   │   │   └── api/        # Base API
│   │   │   │       ├── base_router.py           # Base router
│   │   │   │       ├── base_controller.py       # Base controller
│   │   │   │       └── base_responses.py        # Base responses
│   │   │   │
│   │   │   ├── config/        # Core configurations
│   │   │   │   ├── settings/
│   │   │   │   │   ├── app_settings.py         # App settings
│   │   │   │   │   ├── db_settings.py          # Database settings
│   │   │   │   │   └── cache_settings.py       # Cache settings
│   │   │   │   │
│   │   │   │   ├── logging/
│   │   │   │   │   ├── log_config.py           # Logging config
│   │   │   │   │   └── log_formatter.py        # Log formatters
│   │   │   │   │
│   │   │   │   └── middleware/
│   │   │   │       ├── auth_middleware.py      # Auth middleware
│   │   │   │       ├── cors_middleware.py      # CORS config
│   │   │   │       └── logging_middleware.py   # Logging middleware
│   │   │   │
│   │   │   ├── infrastructure/ # Core infrastructure
│   │   │   │   ├── database/
│   │   │   │   │   ├── connection.py           # DB connection
│   │   │   │   │   └── session.py             # DB session
│   │   │   │   │
│   │   │   │   ├── cache/
│   │   │   │   │   ├── redis_cache.py         # Redis implementation
│   │   │   │   │   └── cache_manager.py       # Cache management
│   │   │   │   │
│   │   │   │   └── messaging/
│   │   │   │       ├── kafka/
│   │   │   │       │   ├── producer.py         # Kafka producer
│   │   │   │       │   └── consumer.py         # Kafka consumer
│   │   │   │       │
│   │   │   │       └── rabbitmq/
│   │   │   │           ├── publisher.py        # RMQ publisher
│   │   │   │           └── subscriber.py       # RMQ subscriber
│   │   │   │
│   │   │   └── utils/         # Core utilities
│   │   │       ├── decorators/
│   │   │       │   ├── retry.py               # Retry decorator
│   │   │       │   ├── cache.py              # Cache decorator
│   │   │       │   └── validate.py           # Validation decorator
│   │   │       │
│   │   │       ├── security/
│   │   │       │   ├── jwt.py                # JWT handling
│   │   │       │   ├── password.py           # Password handling
│   │   │       │   └── encryption.py         # Data encryption
│   │   │       │
│   │   │       └── validation/
│   │   │           ├── validators.py          # Data validators
│   │   │           └── schemas.py            # Validation schemas
│   │   │
│   │   └── tests/            # Core tests
│   │       ├── base/
│   │       │   ├── test_commands.py
│   │       │   └── test_queries.py
│   │       │
│   │       └── infrastructure/
│   │           ├── test_database.py
│   │           └── test_messaging.py
│   │
│   └── services/              # Business services
│       └── [service_name]/    # Each microservice
│           ├── src/
│           │   ├── api/       # API Layer
│           │   │   ├── v1/    # API version 1
│           │   │   │   ├── endpoints/
│           │   │   │   │   └── [feature]/
│           │   │   │   │       ├── command_endpoints.py    # Command endpoints
│           │   │   │   │       └── query_endpoints.py      # Query endpoints
│           │   │   │   │
│           │   │   │   ├── request/
│           │   │   │   │   └── [feature]/
│           │   │   │   │       ├── command_requests.py     # Command DTOs
│           │   │   │   │       └── query_requests.py       # Query DTOs
│           │   │   │   │
│           │   │   │   ├── response/
│           │   │   │   │   └── [feature]/
│           │   │   │   │       ├── command_responses.py    # Command responses
│           │   │   │   │       └── query_responses.py      # Query responses
│           │   │   │   │
│           │   │   │   └── router.py                      # API router
│           │   │   │
│           │   │   ├── middlewares/
│           │   │   │   ├── error_handler.py               # Error handling
│           │   │   │   ├── request_validator.py           # Request validation
│           │   │   │   └── response_formatter.py          # Response formatting
│           │   │   │
│           │   │   └── dependencies.py                    # API dependencies
│           │   │
│           │   ├── application/  # Application Layer
│           │   │   ├── commands/ # CQRS Commands
│           │   │   │   └── [feature]/
│           │   │   │       ├── handlers/
│           │   │   │       │   ├── create_handler.py      # Create handler
│           │   │   │       │   ├── update_handler.py      # Update handler
│           │   │   │       │   └── delete_handler.py      # Delete handler
│           │   │   │       │
│           │   │   │       ├── validators/
│           │   │   │       │   └── command_validator.py   # Command validation
│           │   │   │       │
│           │   │   │       └── commands.py               # Command definitions
│           │   │   │
│           │   │   ├── queries/  # CQRS Queries
│           │   │   │   └── [feature]/
│           │   │   │       ├── handlers/
│           │   │   │       │   ├── get_handler.py         # Get handler
│           │   │   │       │   └── list_handler.py        # List handler
│           │   │   │       │
│           │   │   │       ├── validators/
│           │   │   │       │   └── query_validator.py     # Query validation
│           │   │   │       │
│           │   │   │       └── queries.py                # Query definitions
│           │   │   │
│           │   │   └── events/   # Domain Events
│           │   │       └── [feature]/
│           │   │           ├── handlers/
│           │   │           │   └── event_handler.py       # Event handlers
│           │   │           │
│           │   │           └── events.py                 # Event definitions
│           │   │
│           │   ├── domain/     # Domain Layer
│           │   │   ├── models/  # Domain models
│           │   │   │   └── [feature]/
│           │   │   │       ├── entities.py              # Domain entities
│           │   │   │       └── value_objects.py         # Value objects
│           │   │   │
│           │   │   ├── repositories/  # Repository interfaces
│           │   │   │   └── [feature]/
│           │   │   │       ├── read_repository.py       # Read interface
│           │   │   │       └── write_repository.py      # Write interface
│           │   │   │
│           │   │   └── exceptions/  # Domain exceptions
│           │   │       └── [feature]_exceptions.py      # Feature exceptions
│           │   │
│           │   └── infrastructure/ # Infrastructure Layer
│           │       ├── database/   # Database
│           │       │   ├── models/ # Database models
│           │       │   │   └── [feature]/
│           │       │   │       ├── read_models.py       # Read models
│           │       │   │       └── write_models.py      # Write models
│           │       │   │
│           │       │   ├── repositories/ # Repository implementations
│           │       │   │   └── [feature]/
│           │       │   │       ├── read_repository.py   # Read implementation
│           │       │   │       └── write_repository.py  # Write implementation
│           │       │   │
│           │       │   └── migrations/  # Database migrations
│           │       │       └── versions/
│           │       │           └── [timestamp]_[description].py
│           │       │
│           │       ├── messaging/  # Message handling
│           │       │   ├── publishers/
│           │       │   │   └── [event]_publisher.py    # Event publishing
│           │       │   │
│           │       │   └── consumers/
│           │       │       └── [event]_consumer.py     # Event consuming
│           │       │
│           │       └── external/   # External services
│           │           └── clients/
│           │               └── [service]_client.py     # External clients
│           │
│           ├── tests/            # Service tests
│           │   ├── api/          # API tests
│           │   │   └── v1/
│           │   │       └── test_[feature].py
│           │   │
│           │   ├── application/  # Application tests
│           │   │   ├── commands/
│           │   │   │   └── test_[command].py
│           │   │   └── queries/
│           │   │       └── test_[query].py
│           │   │
│           │   ├── domain/      # Domain tests
│           │   │   └── test_[model].py
│           │   │
│           │   └── infrastructure/  # Infrastructure tests
│           │       └── test_repository.py
│           │
│           ├── config/          # Service configuration
│           │   ├── development/
│           │   │   ├── app.env
│           │   │   └── db.env
│           │   └── production/
│           │       ├── app.env
│           │       └── db.env
│           │
│           ├── Dockerfile      # Service Dockerfile
│           └── requirements/   # Python dependencies
│               ├── base.txt
│               ├── dev.txt
│               └── prod.txt
│
├── infrastructure/           # Infrastructure and DevOps
│   ├── docker/              # Docker configurations
│   │   ├── development/     # Development environment
│   │   │   ├── services/   # Service containers
│   │   │   │   ├── backend/
│   │   │   │   │   ├── Dockerfile.dev           # Dev Dockerfile
│   │   │   │   │   └── entrypoint.sh            # Container entry
│   │   │   │   │
│   │   │   │   ├── database/
│   │   │   │   │   ├── Dockerfile               # DB container
│   │   │   │   │   └── init.sql                 # DB initialization
│   │   │   │   │
│   │   │   │   └── cache/
│   │   │   │       └── redis.conf               # Redis config
│   │   │   │
│   │   │   ├── monitoring/ # Development monitoring
│   │   │   │   ├── prometheus/
│   │   │   │   │   └── prometheus.dev.yml       # Dev metrics
│   │   │   │   │
│   │   │   │   └── grafana/
│   │   │   │       └── dashboards/
│   │   │   │           └── dev-dashboard.json   # Dev dashboard
│   │   │   │
│   │   │   └── docker-compose.dev.yml          # Dev orchestration
│   │   │
│   │   └── production/     # Production environment
│   │       ├── services/   # Production services
│   │       │   ├── backend/
│   │       │   │   ├── Dockerfile.prod          # Prod Dockerfile
│   │       │   │   └── entrypoint.sh            # Container entry
│   │       │   │
│   │       │   ├── nginx/
│   │       │   │   ├── Dockerfile               # Nginx container
│   │       │   │   ├── nginx.conf               # Nginx config
│   │       │   │   └── conf.d/
│   │       │   │       └── default.conf         # Site config
│   │       │   │
│   │       │   └── cache/
│   │       │       └── redis.prod.conf          # Redis prod
│   │       │
│   │       ├── monitoring/ # Production monitoring
│   │       │   ├── prometheus/
│   │       │   │   └── prometheus.prod.yml      # Prod metrics
│   │       │   │
│   │       │   └── grafana/
│   │       │       └── dashboards/
│   │       │           └── prod-dashboard.json  # Prod dashboard
│   │       │
│   │       └── docker-compose.prod.yml         # Prod orchestration
│   │
│   ├── kubernetes/         # Kubernetes configurations
│   │   ├── base/          # Base configurations
│   │   │   ├── namespaces/
│   │   │   │   ├── backend.yaml               # Backend namespace
│   │   │   │   └── monitoring.yaml            # Monitoring namespace
│   │   │   │
│   │   │   ├── deployments/
│   │   │   │   ├── backend/
│   │   │   │   │   ├── deployment.yaml        # Backend deployment
│   │   │   │   │   └── service.yaml           # Backend service
│   │   │   │   │
│   │   │   │   └── monitoring/
│   │   │   │       ├── prometheus.yaml        # Prometheus deploy
│   │   │   │       └── grafana.yaml           # Grafana deploy
│   │   │   │
│   │   │   ├── configs/
│   │   │   │   ├── backend-config.yaml        # Backend config
│   │   │   │   └── monitoring-config.yaml     # Monitoring config
│   │   │   │
│   │   │   └── secrets/
│   │   │       ├── backend-secrets.yaml       # Backend secrets
│   │   │       └── db-secrets.yaml            # Database secrets
│   │   │
│   │   ├── overlays/      # Environment overlays
│   │   │   ├── development/
│   │   │   │   ├── kustomization.yaml         # Dev customization
│   │   │   │   └── patches/
│   │   │   │       └── deployment-patch.yaml  # Dev patches
│   │   │   │
│   │   │   └── production/
│   │   │       ├── kustomization.yaml         # Prod customization
│   │   │       └── patches/
│   │   │           └── deployment-patch.yaml  # Prod patches
│   │   │
│   │   └── scripts/      # K8s management scripts
│   │       ├── deploy.sh                      # Deployment script
│   │       ├── rollback.sh                    # Rollback script
│   │       └── scale.sh                       # Scaling script
│   │
│   ├── monitoring/        # Monitoring stack
│   │   ├── prometheus/    # Metrics collection
│   │   │   ├── rules/
│   │   │   │   ├── backend-alerts.yml         # Backend alerts
│   │   │   │   └── service-alerts.yml         # Service alerts
│   │   │   │
│   │   │   └── recording/
│   │   │       └── backend-metrics.yml        # Custom metrics
│   │   │
│   │   ├── grafana/      # Visualization
│   │   │   ├── dashboards/
│   │   │   │   ├── system/
│   │   │   │   │   ├── resources.json         # Resource metrics
│   │   │   │   │   └── performance.json       # Performance metrics
│   │   │   │   │
│   │   │   │   └── business/
│   │   │   │       └── kpis.json             # Business metrics
│   │   │   │
│   │   │   └── datasources/
│   │   │       └── prometheus.yml            # Data source config
│   │   │
│   │   ├── alertmanager/ # Alert management
│   │   │   ├── config.yml                    # Alert config
│   │   │   └── templates/
│   │   │       └── notification.tmpl         # Alert templates
│   │   │
│   │   └── logging/      # Log management
│   │       ├── fluentd/
│   │       │   └── fluent.conf              # Log collection
│   │       │
│   │       └── elasticsearch/
│   │           └── elasticsearch.yml        # Log storage
│   │
│   └── ci-cd/            # CI/CD pipelines
│       ├── github/
│       │   └── workflows/
│       │       ├── quality/
│       │       │   ├── lint.yml             # Code linting
│       │       │   ├── test.yml             # Testing
│       │       │   └── security.yml         # Security scan
│       │       │
│       │       ├── build/
│       │       │   ├── mobile.yml           # Mobile build
│       │       │   └── backend.yml          # Backend build
│       │       │
│       │       └── deploy/
│       │           ├── staging.yml          # Staging deploy
│       │           └── production.yml       # Production deploy
│       │
│       └── scripts/     # CI/CD scripts
│           ├── build/
│           │   ├── build-mobile.sh         # Mobile build
│           │   └── build-backend.sh        # Backend build
│           │
│           ├── test/
│           │   ├── run-unit-tests.sh       # Unit tests
│           │   └── run-integration-tests.sh # Integration tests
│           │
│           └── deploy/
│               ├── deploy-staging.sh       # Staging deployment
│               └── deploy-production.sh    # Production deployment
 

