from typing import (
  Any, AsyncGenerator, Callable, ClassVar, Dict, Generator, List, Literal, 
  Optional, Tuple, TypeVar, Type, TypeAlias, Union, TypedDict, Set
)
from pydantic import (
  BaseModel, Field
)

from enum import Enum, auto
from dataclasses import dataclass, field, asdict, replace

from collections import defaultdict

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

UserQueryCategory: TypeAlias = Literal["car_control", "car_manual", "general"]
