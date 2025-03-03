# Core Domain Layer
# ================
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Protocol, TypeVar, Generic, Any
from uuid import UUID, uuid4
import json
import logging
import time
import aio_pika
import asyncpg

logger = logging.getLogger(__name__)

# Domain Exceptions
class DomainException(Exception):
    pass

class ValidationError(DomainException):
    pass

class BusinessRuleViolation(DomainException):
    pass

# Example: OrderError, ProductError
class _ENTITY_NAME_Error(DomainException):
    pass

# Example: OrderNotFoundError
class _ENTITY_NAME_NotFoundError(_ENTITY_NAME_Error):
    pass

# Value Objects
# Example: Money(amount=Decimal('10.00'), currency='USD')
@dataclass(frozen=True)
class _VALUE_OBJECT_NAME_:
    _VALUE_OBJECT_FIELDS_  # Example: amount: Decimal, currency: str

    def __post_init__(self) -> None:
        if not self._validation_rules_:  # Example: self.amount > 0
            raise ValidationError(_VALIDATION_MESSAGE_)

# Entities
# Example: Product(id=uuid4(), name='Book', price=Money(10, 'USD'))
@dataclass
class _ENTITY_NAME_:
    id: UUID
    _ENTITY_FIELDS_  # Example: name: str, price: Money
    created_at: datetime
    version: int = 1

    @staticmethod
    def create(_CREATION_PARAMS_) -> '_ENTITY_NAME_':  # Example: name: str, price: Money
        if not _CREATION_VALIDATION_:  # Example: name and price.amount > 0
            raise ValidationError("_ENTITY_NAME_ validation failed")
        return _ENTITY_NAME_(
            id=uuid4(),
            _ENTITY_CREATION_FIELDS_,  # Example: name=name, price=price
            created_at=datetime.utcnow()
        )

# Example: OrderStatus.PENDING, OrderStatus.COMPLETED
class _ENTITY_NAME_Status(Enum):
    _STATUS_ENUM_VALUES_  # Example: PENDING = "pending"

# Example: Order with OrderItems
@dataclass
class _AGGREGATE_ROOT_:
    id: UUID
    _AGGREGATE_FIELDS_  # Example: customer_id: UUID, items: List[OrderItem]
    version: int = 1

    def _validate_business_rules(self) -> None:
        if not _BUSINESS_RULES_:  # Example: len(self.items) > 0
            raise BusinessRuleViolation(_BUSINESS_RULE_MESSAGE_)

# Domain Events
@dataclass
class DomainEvent:
    event_id: UUID
    occurred_on: datetime
    version: int = 1

# Example: OrderCreatedEvent
@dataclass
class _ENTITY_NAME_CreatedEvent(DomainEvent):
    _entity_name_lower_id: UUID  # Example: order_id: UUID
    _EVENT_FIELDS_  # Example: customer_id: UUID

# Domain Services Layer
# ====================

# Specifications
T = TypeVar('T')

class Specification(Protocol[T]):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        pass

# Example: OrderSpecification
class _ENTITY_NAME_Specification(Specification[_ENTITY_NAME_]):
    @abstractmethod
    def is_satisfied_by(self, _entity_name_lower_: _ENTITY_NAME_) -> bool:
        pass

# Domain Service Interfaces
# Example: OrderPolicy
class _ENTITY_NAME_Policy(Protocol):
    def can_create__entity_name_lower_(self, _VALIDATION_PARAMS_) -> bool:  # Example: customer_id: UUID
        ...

# Application Layer
# ================

# DTOs
# Example: CreateOrderDTO(customer_id=uuid4(), items=[...])
@dataclass
class Create_ENTITY_NAME_DTO:
    _DTO_FIELDS_  # Example: customer_id: UUID, items: List[dict]

@dataclass
class _ENTITY_NAME_ResponseDTO:
    id: UUID
    _RESPONSE_DTO_FIELDS_  # Example: status: str, total: dict

# Ports
class _ENTITY_NAME_Repository(ABC):
    @abstractmethod
    async def save(self, _entity_name_lower_: _ENTITY_NAME_) -> None:
        pass

    @abstractmethod
    async def update(self, _entity_name_lower_: _ENTITY_NAME_) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, _entity_name_lower_id: UUID) -> Optional[_ENTITY_NAME_]:
        pass

class EventPublisher(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass

class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> 'UnitOfWork':
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

# Use Cases
class UseCase(Generic[T]):
    @abstractmethod
    async def execute(self, input_dto: T) -> Any:
        pass

# Example: CreateOrderUseCase
class Create_ENTITY_NAME_UseCase(UseCase[Create_ENTITY_NAME_DTO]):
    def __init__(
        self,
        repository: _ENTITY_NAME_Repository,
        policy: _ENTITY_NAME_Policy,
        event_publisher: EventPublisher,
        unit_of_work: UnitOfWork
    ):
        self._repository = repository
        self._policy = policy
        self._event_publisher = event_publisher
        self._uow = unit_of_work

    async def execute(self, input_dto: Create_ENTITY_NAME_DTO) -> _ENTITY_NAME_ResponseDTO:
        try:
            async with self._uow:
                _entity_name_lower_ = _ENTITY_NAME_.create(
                    _CREATION_MAPPING_  # Example: customer_id=input_dto.customer_id
                )

                await self._repository.save(_entity_name_lower_)

                event = _ENTITY_NAME_CreatedEvent(
                    event_id=uuid4(),
                    occurred_on=datetime.utcnow(),
                    _entity_name_lower_id=_entity_name_lower_.id,
                    _EVENT_MAPPING_  # Example: customer_id=input_dto.customer_id
                )

                await self._event_publisher.publish(event)
                await self._uow.commit()

                return _ENTITY_NAME_ResponseDTO(
                    _RESPONSE_MAPPING_  # Example: id=_entity_name_lower_.id
                )
        except Exception as e:
            await self._uow.rollback()
            raise

# Application Services Layer
# =========================

def log_execution_time(logger: logging.Logger):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                logger.info(f"{func.__name__} completed in {time.time() - start:.2f}s")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed: {str(e)}")
                raise
        return wrapper
    return decorator

# Example: OrderApplicationService
class _ENTITY_NAME_ApplicationService:
    def __init__(
        self,
        create__entity_name_lower__use_case: Create_ENTITY_NAME_UseCase,
        _entity_name_lower__repository: _ENTITY_NAME_Repository,
        unit_of_work: UnitOfWork
    ):
        self._create__entity_name_lower__use_case = create__entity_name_lower__use_case
        self._repository = _entity_name_lower__repository
        self._uow = unit_of_work

    @log_execution_time(logger)
    async def create__entity_name_lower_(
        self, 
        input_dto: Create_ENTITY_NAME_DTO
    ) -> _ENTITY_NAME_ResponseDTO:
        try:
            return await self._create__entity_name_lower__use_case.execute(input_dto)
        except BusinessRuleViolation as e:
            logger.warning(f"Business rule violation: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating _entity_name_lower_: {e}")
            raise

# Infrastructure Layer
# ===================

class RabbitMQEventPublisher(EventPublisher):
    def __init__(
        self,
        connection: aio_pika.Connection,
        exchange_name: str = '_EVENT_EXCHANGE_'  # Example: 'order_events'
    ):
        self._connection = connection
        self._exchange_name = exchange_name
        self._channel = None
        self._exchange = None

    async def publish(self, event: DomainEvent) -> None:
        try:
            if not self._channel:
                self._channel = await self._connection.channel()
                self._exchange = await self._channel.declare_exchange(
                    name=self._exchange_name,
                    type='topic',
                    durable=True
                )
            
            event_data = {
                'event_id': str(event.event_id),
                'event_type': event.__class__.__name__,
                'data': {
                    k: str(v) if isinstance(v, (UUID, datetime)) else v
                    for k, v in event.__dict__.items()
                    if k not in ['event_id', 'occurred_on', 'version']
                }
            }

            await self._exchange.publish(
                aio_pika.Message(
                    body=json.dumps(event_data).encode(),
                    content_type='application/json',
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=f"_ENTITY_NAME_LOWER_.{event.__class__.__name__.lower()}"
            )

        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            raise

    async def close(self) -> None:
        if self._channel:
            await self._channel.close()

class Postgres_ENTITY_NAME_Repository(_ENTITY_NAME_Repository):
    def __init__(self, db_pool):
        self._db_pool = db_pool

    async def save(self, _entity_name_lower_: _ENTITY_NAME_) -> None:
        async with self._db_pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    """
                    INSERT INTO _TABLE_NAME_ (
                        _TABLE_COLUMNS_  -- Example: id, name, status
                    ) VALUES (_PLACEHOLDER_VALUES_)  -- Example: $1, $2, $3
                    """,
                    _QUERY_PARAMS_  # Example: _entity_name_lower_.id
                )

class PostgresUnitOfWork(UnitOfWork):
    def __init__(self, db_pool):
        self._db_pool = db_pool
        self._conn = None
        self._transaction = None

    async def __aenter__(self) -> 'PostgresUnitOfWork':
        self._conn = await self._db_pool.acquire()
        self._transaction = self._conn.transaction()
        await self._transaction.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type:
                await self._transaction.rollback()
            else:
                await self._transaction.commit()
        finally:
            await self._db_pool.release(self._conn)

    async def commit(self) -> None:
        await self._transaction.commit()

    async def rollback(self) -> None:
        await self._transaction.rollback()

# API Layer
# =========

# Example: OrderController
class _ENTITY_NAME_Controller:
    def __init__(self, _entity_name_lower__service: _ENTITY_NAME_ApplicationService):
        self._service = _entity_name_lower__service

    async def create__entity_name_lower_(self, request_data: dict) -> dict:
        try:
            input_dto = Create_ENTITY_NAME_DTO(
                _DTO_MAPPING_  # Example: customer_id=UUID(request_data['customer_id'])
            )

            result = await self._service.create__entity_name_lower_(input_dto)
            
            return {
                'id': str(result.id),
                _RESPONSE_JSON_MAPPING_  # Example: 'status': result.status
            }
        except DomainException as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Database Schema
# ==============

SCHEMA_SQL = """
CREATE TABLE _TABLE_NAME_ (  -- Example: orders
    id UUID PRIMARY KEY,
    _TABLE_COLUMNS_DEFINITION_,  -- Example: customer_id UUID NOT NULL
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX _INDEX_NAME_ ON _TABLE_NAME_(_INDEX_COLUMNS_);  -- Example: idx_orders_customer_id
"""

# Application Setup
# ================

async def create_app():
    # Infrastructure setup
    db_pool = await asyncpg.create_pool(
        user='_DB_USER_',  # Example: 'postgres'
        password='_DB_PASSWORD_',
        database='_DB_NAME_',
        host='_DB_HOST_'
    )
    
    rabbitmq_conn = await aio_pika.connect_robust(
        "amqp://_MQ_USER_:_MQ_PASSWORD_@_MQ_HOST_:_MQ_PORT_/"
    )

    # Create instances
    repository = Postgres_ENTITY_NAME_Repository(db_pool)
    event_publisher = RabbitMQEventPublisher(rabbitmq_conn)
    unit_of_work = PostgresUnitOfWork(db_pool)
    
    # Create use case
    create__entity_name_lower__use_case = Create_ENTITY_NAME_UseCase(
        repository=repository,
        policy=Default_ENTITY_NAME_Policy(),
        event_publisher=event_publisher,
        unit_of_work=unit_of_work
    )

    # Create application service
    app_service = _ENTITY_NAME_ApplicationService(
        create__entity_name_lower__use_case=create__entity_name_lower__use_case,
        _entity_name_lower__repository=repository,
        unit_of_work=unit_of_work
    )

    # Create controller
    controller = _ENTITY_NAME_Controller(app_service)

    return controller, db_pool, rabbitmq_conn
  

# Example Usage
# =============

async def main():
    try:
        controller, db_pool, rabbitmq_conn = await create_app()
        
        # Example request data
        request_data = {
            '_REQUEST_FIELDS_': '_VALUES_'  # Example: 'customer_id': 'uuid-string'
        }

        # Create entity
        response = await controller.create__entity_name_lower_(request_data)
        print(f"Created: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        await db_pool.close()
        await rabbitmq_conn.close()

# Tests
# =====

import pytest
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_create__entity_name_lower_():
    # Arrange
    mock_repo = Mock(spec=_ENTITY_NAME_Repository)
    mock_repo.save = AsyncMock()
    
    mock_policy = Mock(spec=_ENTITY_NAME_Policy)
    mock_policy.can_create__entity_name_lower_.return_value = True
    
    mock_publisher = Mock(spec=EventPublisher)
    mock_publisher.publish = AsyncMock()
    
    mock_uow = Mock(spec=UnitOfWork)
    mock_uow.__aenter__ = AsyncMock(return_value=mock_uow)
    mock_uow.__aexit__ = AsyncMock()
    mock_uow.commit = AsyncMock()
    
    use_case = Create_ENTITY_NAME_UseCase(
        repository=mock_repo,
        policy=mock_policy,
        event_publisher=mock_publisher,
        unit_of_work=mock_uow
    )

    input_dto = Create_ENTITY_NAME_DTO(
        _TEST_DTO_FIELDS_  # Example: customer_id=uuid4()
    )

    # Act
    result = await use_case.execute(input_dto)

    # Assert
    assert result is not None
    assert isinstance(result.id, UUID)
    mock_repo.save.assert_called_once()
    mock_publisher.publish.assert_called_once()

# Template Documentation
# ====================

"""
Placeholder Replacement Guide:

1. Entity Definition:
   _ENTITY_NAME_ -> Your entity name (e.g., Order, Product)
   _ENTITY_FIELDS_ -> Entity attributes
   _ENTITY_NAME_LOWER_ -> Lowercase entity name

2. Value Objects:
   _VALUE_OBJECT_NAME_ -> Value object name
   _VALUE_OBJECT_FIELDS_ -> Value object attributes
   _VALIDATION_RULES_ -> Validation logic

3. Database:
   _TABLE_NAME_ -> Database table name
   _TABLE_COLUMNS_ -> Table columns
   _INDEX_NAME_ -> Index names

4. Events:
   _EVENT_EXCHANGE_ -> RabbitMQ exchange name
   _EVENT_FIELDS_ -> Event attributes

5. DTOs:
   _DTO_FIELDS_ -> Input DTO fields
   _RESPONSE_DTO_FIELDS_ -> Response DTO fields
   _DTO_MAPPING_ -> Request to DTO mapping

6. Infrastructure:
   _DB_USER_ -> Database username
   _MQ_USER_ -> RabbitMQ username
   etc.

Implementation Steps:
1. Replace all placeholders with actual values
2. Add domain-specific business rules
3. Implement custom validations
4. Add specific repository methods
5. Define proper database schema
6. Add additional use cases as needed
"""

# Example Implementation for Order Domain
# ====================================

"""
Example replacements:
- _ENTITY_NAME_ -> Order
- _ENTITY_NAME_LOWER_ -> order
- _VALUE_OBJECT_NAME_ -> Money
- _TABLE_NAME_ -> orders
- _EVENT_EXCHANGE_ -> order_events

See the test file for a complete example implementation.
"""

if __name__ == "__main__":
    asyncio.run(main())