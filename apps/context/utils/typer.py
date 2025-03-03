import inspect
from typing import (
  Any, AsyncGenerator, Callable, ClassVar, Dict, Generator, List, Literal, 
  Optional, Tuple, TypeVar, Type, TypeAlias, Union, Set, Iterator,
  get_type_hints, Annotated
)

from typing_extensions import TypedDict

from pydantic import (
  BaseModel, Field, ConfigDict, create_model, field_validator
)

from enum import Enum, auto
from dataclasses import dataclass, field, asdict, replace

from collections import defaultdict
#*==============================================================================

# Create a TypeVar bound to TypedDict to ensure type safety
TypedDictSchema = TypeVar('TypedDictSchema', bound=TypedDict)

def my_fn(schema: Type[TypedDictSchema]) -> None:
    type_hints = get_type_hints(schema, include_extras=True)
    
    for field_name, field_type in type_hints.items():
        if hasattr(field_type, "__metadata__"):
            print(f"Field: {field_name}")
            print(f"Type: {field_type.__origin__}")
            print(f"Metadata: {field_type.__metadata__}")
            
#*==============================================================================

@dataclass(order=True)
class _Employee:
    # Sort by last_name first, then first_name using field(init=False)
    sort_index: str = field(init=False, repr=False)
    
    first_name: str = field(default="John")
    last_name: str = field(default="Doe")
    skills: List[str] = field(default_factory=list)  # Mutable default
    nickname: Optional[str] = field(
        default=None,
        compare=False,  # Exclude from comparisons
        repr=False      # Exclude from string representation
    )
    
    def __post_init__(self):
        # Set sort_index after initialization
        self.sort_index = f"{self.last_name}_{self.first_name}"
        
        # Capitalize names
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        
        # Set default nickname
        if self.nickname is None:
            self.nickname = self.first_name[:3]
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def add_skill(self, skill: str) -> None:
        if skill not in self.skills:
            self.skills.append(skill)

class EnumCustom(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower().replace('_', ' ').replace(' ', '_')
    
    def __str__(self):
        return self.value
        
    def __repr__(self):
        return self.value

def parent_enum(cls):
    """Decorator to add string name to provider enum classes"""
    setattr(cls, 'name', cls.__name__)
    return cls

#*==============================================================================

T = TypeVar('T', bound='BaseModel')

def get_field_default(schema: Type[T], field: Union[str, Enum]) -> Any:
    """
    Get the default value of a field from a Pydantic schema.
    
    Args:
        schema: The Pydantic model class
        field: Either a string field name or an Enum value representing the field
        
    Returns:
        The default value of the field, or None if no default exists
        
    Raises:
        KeyError: If the field doesn't exist in the schema
        ValueError: If the field has no default value set
    """
    # Get the actual field name - using the enum value instead of name
    field_name = str(field) if isinstance(field, Enum) else field
    
    try:
        field_info = schema.model_fields[field_name]
    except KeyError:
        raise KeyError(f"Field '{field_name}' not found in schema {schema.__name__}")
    
    # Check if field has a default value
    if field_info.default == ... and field_info.default_factory is None:
        raise ValueError(f"Field '{field_name}' has no default value")
    
    # Return default factory result if it exists
    if field_info.default_factory is not None:
        return field_info.default_factory()
    
    return field_info.default

# Helper function to get multiple field defaults at once
def get_fields_defaults(schema: Type[T], fields: list[Union[str, Enum]]) -> dict[str, Any]:
    """
    Get default values for multiple fields from a Pydantic schema.
    
    Args:
        schema: The Pydantic model class
        fields: List of field names or Enum values
        
    Returns:
        Dictionary mapping field names to their default values
    """
    return {
        str(field) if isinstance(field, Enum) else field: get_field_default(schema, field)
        for field in fields
    }

#*==============================================================================

class CaseInsensitiveDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        for k, v in dict(*args, **kwargs).items():
            self[k] = k.lower()  # Store the lowercase key as the value
            
    def __getitem__(self, key):
        return super().__getitem__(key.lower())
    
    def __setitem__(self, key, value):
        if isinstance(value, str):
            super().__setitem__(key.lower(), value.lower())
        else:
            super().__setitem__(key.lower(), value)

#*==============================================================================

YAMLValue: TypeAlias = Union[str, Dict[str, 'YAMLValue']]
Prompts: TypeAlias = Dict[str, YAMLValue]
