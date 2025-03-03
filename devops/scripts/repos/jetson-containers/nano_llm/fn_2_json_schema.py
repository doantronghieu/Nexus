"""
Function to JSON Schema Converter
A modular implementation for converting Python functions with type hints and Pydantic models to JSON Schema.
"""

from typing import (
    List, Dict, Optional, Union, Tuple, Set, 
    get_type_hints, Type, Any, get_args, get_origin
)
from dataclasses import dataclass
from inspect import signature, Parameter
import pydantic
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, date
import warnings
from functools import lru_cache
import json

# Custom Exceptions
class SchemaConversionError(Exception):
    """Base exception for schema conversion errors"""
    pass

class ValidationError(SchemaConversionError):
    """Validation specific errors"""
    pass

class TypeConversionError(SchemaConversionError):
    """Type conversion specific errors"""
    pass

# Custom JSON Encoder
class SchemaEncoder(json.JSONEncoder):
    """Custom JSON encoder for schema objects"""
    def default(self, obj):
        if hasattr(obj, '__class__'):
            if obj.__class__.__name__ == 'PydanticUndefinedType':
                return None
            if isinstance(obj, set):
                return list(obj)
            if isinstance(obj, Enum):
                return obj.value
        return super().default(obj)

# Core Data Models
@dataclass
class SchemaContext:
    """Context object for schema conversion process"""
    type_registry: 'TypeRegistry'
    current_depth: int = 0
    max_depth: int = 10

@dataclass
class FieldMetadata:
    """Container for field metadata"""
    type_hint: Type
    description: Optional[str] = None
    default: Any = None
    validators: List[Any] = None
    required: bool = True

    @classmethod
    def from_parameter(cls, param: Parameter, type_hint: Type) -> 'FieldMetadata':
        """Create FieldMetadata from a Parameter object"""
        # Check if parameter is required (no default value)
        required = param.default == Parameter.empty
        default = None
        validators = []
        description = None
        
        # Handle Pydantic Field
        if isinstance(param.default, pydantic.fields.FieldInfo):
            field_info = param.default
            
            # Check if field is required
            required = (not hasattr(field_info, 'default') or 
                       field_info.default is ... or 
                       field_info.default is None or
                       field_info.default == 'undefined')
            
            # Get validators
            validators = getattr(field_info, 'metadata', []) or []
            
            # Get description
            description = getattr(field_info, 'description', None)
            
            # Handle default value
            if not required:
                if hasattr(field_info, 'default_factory') and field_info.default_factory:
                    try:
                        default = field_info.default_factory()
                    except Exception:
                        default = None
                else:
                    default = field_info.default
        else:
            # Handle regular parameter default
            if not required and param.default is not None:
                default = param.default
        
        return cls(
            type_hint=type_hint,
            description=description,
            default=default,
            validators=validators,
            required=required
        )
                
# Type Registry System
class TypeRegistry:
    """Enhanced registry for custom type mappings"""
    
    def __init__(self):
        self._type_mappings: Dict[Type, callable] = {}
        self._initialize_defaults()
    
    def _initialize_defaults(self):
        """Initialize default type mappings"""
        default_mappings = {
            datetime: lambda: {"type": "string", "format": "date-time"},
            date: lambda: {"type": "string", "format": "date"},
            str: lambda: {"type": "string"},
            int: lambda: {"type": "integer", "format": "int64"},
            float: lambda: {"type": "number", "format": "float"},
            bool: lambda: {"type": "boolean"},
            Any: lambda: {"type": "any"}
        }
        for type_, schema_gen in default_mappings.items():
            self.register(type_, schema_gen)
    
    def register(self, python_type: Type, schema_generator: callable):
        """Register a custom type mapping"""
        if not callable(schema_generator):
            raise TypeError("Schema generator must be callable")
        self._type_mappings[python_type] = schema_generator
    
    def get_schema(self, type_hint: Type, context: SchemaContext) -> Optional[dict]:
        """Get schema for a registered type"""
        if type_hint in self._type_mappings:
            return self._type_mappings[type_hint]()
        return None

# Schema Generators
class SchemaGenerator:
    """Base class for schema generation"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        """Generate schema for a type"""
        if context.current_depth >= context.max_depth:
            return {"type": "any"}
            
        # Check type registry first
        schema = context.type_registry.get_schema(type_hint, context)
        if schema is not None:
            return schema
            
        # Determine the correct generator
        generator = SchemaGenerator._get_generator(type_hint)
        return generator.generate(type_hint, context)
    
    @staticmethod
    def _get_generator(type_hint: Type) -> 'SchemaGenerator':
        """Get appropriate generator for type"""
        origin = get_origin(type_hint)
        
        if origin is Union:
            return UnionSchemaGenerator()
        elif origin in (list, List, set, Set):
            return ArraySchemaGenerator()
        elif origin in (dict, Dict):
            return ObjectSchemaGenerator()
        elif origin in (tuple, Tuple):
            return TupleSchemaGenerator()
        elif isinstance(type_hint, type):
            if issubclass(type_hint, BaseModel):
                return PydanticSchemaGenerator()
            elif issubclass(type_hint, Enum):
                return EnumSchemaGenerator()
        
        return BasicSchemaGenerator()

class BasicSchemaGenerator(SchemaGenerator):
    """Generator for basic types"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        # Handle basic types that weren't caught by type registry
        return {"type": "any"}

class UnionSchemaGenerator(SchemaGenerator):
    """Generator for Union types"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        args = get_args(type_hint)
        non_none_args = [arg for arg in args if arg != type(None)]
        
        if len(non_none_args) == 1:
            schema = SchemaGenerator.generate(non_none_args[0], context)
            if type(None) in args:
                schema['nullable'] = True
            return schema
            
        return {
            "anyOf": [
                SchemaGenerator.generate(arg, context)
                for arg in non_none_args
            ],
            "nullable": type(None) in args
        }

class ArraySchemaGenerator(SchemaGenerator):
    """Generator for array types"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        origin = get_origin(type_hint)
        args = get_args(type_hint)
        
        item_type = args[0] if args else Any
        new_context = SchemaContext(
            type_registry=context.type_registry,
            current_depth=context.current_depth + 1,
            max_depth=context.max_depth
        )
        
        schema = {
            "type": "array",
            "items": SchemaGenerator.generate(item_type, new_context)
        }
        
        if origin in (set, Set):
            schema["uniqueItems"] = True
            
        return schema

class ObjectSchemaGenerator(SchemaGenerator):
    """Generator for object types"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        args = get_args(type_hint)
        
        if not args:
            return {
                "type": "object",
                "additionalProperties": True
            }
            
        key_type, value_type = args
        new_context = SchemaContext(
            type_registry=context.type_registry,
            current_depth=context.current_depth + 1,
            max_depth=context.max_depth
        )
        
        return {
            "type": "object",
            "additionalProperties": SchemaGenerator.generate(value_type, new_context)
        }

class TupleSchemaGenerator(SchemaGenerator):
    """Generator for tuple types"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        args = get_args(type_hint)
        
        if not args or args[-1] is ...:
            item_type = args[0] if args else Any
            return {
                "type": "array",
                "items": SchemaGenerator.generate(item_type, context)
            }
            
        new_context = SchemaContext(
            type_registry=context.type_registry,
            current_depth=context.current_depth + 1,
            max_depth=context.max_depth
        )
        
        return {
            "type": "array",
            "items": [
                SchemaGenerator.generate(arg, new_context)
                for arg in args
            ],
            "minItems": len(args),
            "maxItems": len(args)
        }

class PydanticSchemaGenerator(SchemaGenerator):
    """Generator for Pydantic models"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        schema = type_hint.model_json_schema()
        return SchemaProcessor.normalize_refs(schema)

class EnumSchemaGenerator(SchemaGenerator):
    """Generator for Enum types"""
    
    @staticmethod
    def generate(type_hint: Type, context: SchemaContext) -> dict:
        return {
            "type": "string",
            "enum": [e.value for e in type_hint]
        }

# Schema Processing
class SchemaProcessor:
    """Handles schema processing and cleanup"""
    
    @staticmethod
    def process_schema(schema: dict) -> dict:
        """Process and clean up schema"""
        schema = SchemaProcessor.normalize_refs(schema)
        schema = SchemaProcessor.clean_schema(schema)
        schema = SchemaProcessor.normalize_output(schema)
        return schema

    @staticmethod
    def normalize_refs(schema: dict) -> dict:
        """Normalize schema references"""
        def _normalize(obj):
            if isinstance(obj, dict):
                # Move all definitions to top level
                if '$defs' in obj:
                    if 'definitions' not in schema:
                        schema['definitions'] = {}
                    schema['definitions'].update(obj.pop('$defs'))
                
                # Fix references
                for key, value in list(obj.items()):
                    if key == '$ref':
                        if '#/$defs/' in value:
                            obj[key] = value.replace('/$defs/', '/definitions/')
                    elif isinstance(value, (dict, list)):
                        _normalize(value)
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        _normalize(item)
        
        schema_copy = schema.copy()
        _normalize(schema_copy)
        return schema_copy

    @staticmethod
    def normalize_output(schema: dict) -> dict:
        """Final normalization of schema before output"""
        def _normalize(obj):
            if not isinstance(obj, dict):
                return
            
            # Convert lone nullable to proper type
            if list(obj.keys()) == ['nullable'] and obj['nullable']:
                obj.update({
                    "type": "null"
                })
            
            # Fix anyOf with nullable
            if 'anyOf' in obj:
                non_null = [s for s in obj['anyOf'] if not (isinstance(s, dict) and s.get('nullable'))]
                if len(non_null) < len(obj['anyOf']):
                    obj['anyOf'] = non_null
                    obj['nullable'] = True
            
            # Cleanup default values
            if 'default' in obj and obj['default'] is None:
                del obj['default']
            
            # Normalize required fields
            is_required = obj.pop('required', False)
            if is_required and 'type' in obj:
                obj['required'] = True
            
            # Normalize properties and required fields
            if 'properties' in obj:
                required_props = []
                for prop_name, prop_schema in obj['properties'].items():
                    _normalize(prop_schema)
                    if prop_schema.pop('required', False):
                        required_props.append(prop_name)
                if required_props:
                    obj['required'] = required_props
            
            # Clean up empty objects/arrays
            for key in list(obj.keys()):
                if isinstance(obj[key], (dict, list)) and not obj[key]:
                    del obj[key]
            
            # Recurse into children
            for value in obj.values():
                if isinstance(value, dict):
                    _normalize(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            _normalize(item)
        
        schema_copy = schema.copy()
        _normalize(schema_copy)
        return schema_copy

    @staticmethod
    def clean_schema(schema: dict) -> dict:
        """Clean up schema"""
        def _clean(obj):
            if not isinstance(obj, dict):
                return
            
            # Remove null/empty values
            for key in list(obj.keys()):
                if obj[key] is None or obj[key] == {}:
                    del obj[key]
            
            # Handle Pydantic models
            if 'properties' in obj:
                required_props = []
                for prop_name, prop_schema in obj['properties'].items():
                    _clean(prop_schema)
                    if getattr(prop_schema, 'required', False) or (
                        'default' not in prop_schema and 
                        'nullable' not in prop_schema
                    ):
                        required_props.append(prop_name)
                if required_props:
                    obj['required'] = required_props
            
            # Clean up additionalProperties
            if 'additionalProperties' in obj:
                if obj['additionalProperties'] == {'type': 'any'}:
                    obj['additionalProperties'] = True
            
            # Fix array validations
            if obj.get('type') == 'array':
                if 'min_length' in obj:
                    obj['minItems'] = obj.pop('min_length')
                if 'max_length' in obj:
                    obj['maxItems'] = obj.pop('max_length')
            
            # Recurse into nested objects
            for value in obj.values():
                if isinstance(value, dict):
                    _clean(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            _clean(item)
            
            # Clean up after recursion
            if 'default' in obj and obj['default'] is None:
                del obj['default']
            if 'required' in obj and not obj['required']:
                del obj['required']
        
        schema_copy = schema.copy()
        _clean(schema_copy)
        return schema_copy
            
# Main Converter Class
class FunctionSchemaConverter:
    """Main class for converting functions to JSON schema"""
    
    def __init__(self, type_registry: Optional[TypeRegistry] = None):
        self.type_registry = type_registry or TypeRegistry()
    
    def convert(self, func) -> dict:
        """Convert function to JSON schema"""
        try:
            sig = signature(func)
            type_hints = get_type_hints(func)
            
            context = SchemaContext(type_registry=self.type_registry)
            
            # Process inputs
            inputs = {}
            for name, param in sig.parameters.items():
                if name not in type_hints:
                    warnings.warn(f"Missing type hint for parameter: {name}")
                    continue
                    
                field_metadata = FieldMetadata.from_parameter(param, type_hints[name])
                inputs[name] = self._generate_parameter_schema(field_metadata, context)
            
            # Process output
            outputs = SchemaGenerator.generate(
                type_hints.get('return', Any),
                context
            )
            
            # Create schema
            schema = {
                "function_name": func.__name__,
                "inputs": inputs,
                "outputs": outputs
            }
            
            if func.__doc__:
                schema["function_description"] = func.__doc__.strip()
                
            return SchemaProcessor.process_schema(schema)
            
        except Exception as e:
            raise SchemaConversionError(f"Schema conversion failed: {str(e)}")
    
    def _generate_parameter_schema(
        self,
        field_metadata: FieldMetadata,
        context: SchemaContext
    ) -> dict:
        """Generate schema for a parameter"""
        schema = SchemaGenerator.generate(field_metadata.type_hint, context)
        
        # Add description if present
        if field_metadata.description:
            schema['description'] = field_metadata.description
        
        # Handle required fields and defaults
        if field_metadata.required:
            schema['required'] = True
        elif field_metadata.default is not None:
            schema['default'] = field_metadata.default
        
        # Process validators
        if field_metadata.validators:
            self._process_validators(schema, field_metadata)
        
        return schema

    def _process_validators(self, schema: dict, field_metadata: FieldMetadata):
        """Process field validators"""
        for validator in field_metadata.validators:
            for attr_name in dir(validator):
                if attr_name.startswith('_'):
                    continue
                
                value = getattr(validator, attr_name)
                
                # Map validator attributes to schema properties
                if attr_name == 'min_length':
                    if schema.get('type') == 'array':
                        schema['minItems'] = value
                    else:
                        schema['minLength'] = value
                        
                elif attr_name == 'max_length':
                    if schema.get('type') == 'array':
                        schema['maxItems'] = value
                    else:
                        schema['maxLength'] = value
                        
                elif attr_name == 'pattern':
                    schema['pattern'] = value
                    
                elif attr_name == 'min_items':
                    schema['minItems'] = value
                    
                elif attr_name == 'max_items':
                    schema['maxItems'] = value
                    
                elif attr_name == 'unique_items':
                    schema['uniqueItems'] = value
                    
                elif attr_name == 'multiple_of':
                    schema['multipleOf'] = value
                    
                elif attr_name in ('gt', 'ge', 'lt', 'le'):
                    self._process_numeric_validator(schema, attr_name, value)
    
    @staticmethod
    def _process_numeric_validator(schema: dict, validator_name: str, value: Any):
        """Process numeric validators"""
        if validator_name == 'gt':
            schema['exclusiveMinimum'] = value
        elif validator_name == 'ge':
            schema['minimum'] = value
        elif validator_name == 'lt':
            schema['exclusiveMaximum'] = value
        elif validator_name == 'le':
            schema['maximum'] = value

# Convenience function
def function_to_json_schema(func) -> dict:
    """Convert a function to JSON schema"""
    converter = FunctionSchemaConverter()
    return converter.convert(func)

# Then update the main function
def main():
    """Main function with test cases demonstrating schema conversion"""
    import json
    from typing import Dict, Union, List, Optional, Tuple, Set, Any
    from enum import Enum
    from datetime import datetime
    from pydantic import BaseModel, Field
    
    # Test Case 1: Basic types and validations
    def calculate_score(
        name: str = Field(..., min_length=2, max_length=50),
        age: int = Field(..., ge=0, le=120),
        score: float = Field(..., ge=0.0, le=100.0),
        is_active: bool = True
    ) -> Dict[str, Union[str, float]]:
        """Calculate user score based on age and previous score."""
        pass

    # Test Case 2: Container types
    def process_data(
        items: List[int] = Field(..., min_items=1, max_items=100),
        mapping: Dict[str, float] = Field(default_factory=dict),
        coordinates: Tuple[float, float] = Field(..., description="Latitude and longitude"),
        tags: Set[str] = set()
    ) -> List[Dict[str, Any]]:
        """Process data with various container types."""
        pass

    # Test Case 3: Pydantic models and enums
    class UserRole(str, Enum):
        ADMIN = "admin"
        USER = "user"
        GUEST = "guest"

    class Address(BaseModel):
        street: str
        city: str
        country: str = "Unknown"
        postal_code: Optional[str] = None

    class User(BaseModel):
        id: int
        name: str = Field(..., min_length=2)
        email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        role: UserRole = UserRole.GUEST
        address: Optional[Address] = None

    def update_user(
        user: User,
        new_role: Optional[UserRole] = None,
        update_time: datetime = Field(..., description="Update timestamp")
    ) -> User:
        """Update user information."""
        pass

    # Test Case 4: Complex nested types
    def search_users(
        query: str = Field(..., min_length=3),
        filters: Dict[str, List[Union[str, int]]] = Field(default_factory=dict),
        pagination: Tuple[int, int] = Field((1, 10), description="(page, page_size)"),
        sort_by: Optional[List[Tuple[str, bool]]] = None
    ) -> Dict[str, Union[List[User], int]]:
        """Search users with complex filtering and pagination."""
        pass

    # Test Case 5: Default values and optional fields
    def configure_settings(
        name: str = "default",
        timeout: Optional[int] = 30,
        retries: int = Field(3, ge=0, le=10),
        debug: bool = False,
        custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Configure application settings."""
        pass

    def print_separator():
        print("\n" + "="*80)

    # List of test cases
    test_cases = [
        calculate_score,
        process_data,
        update_user,
        search_users,
        configure_settings
    ]

    # Run test cases
    for test_func in test_cases:
        print_separator()
        print(f"Testing function: {test_func.__name__}")
        print_separator()
        
        try:
            schema = function_to_json_schema(test_func)
            print("Schema generated successfully:")
            print(json.dumps(schema, indent=2, ensure_ascii=False, cls=SchemaEncoder))
        except Exception as e:
            print(f"Error generating schema: {e}")
            import traceback
            print(traceback.format_exc())

    # Test custom type registration
    print_separator()
    print("Testing custom type registration:")
    
    try:
        # Create custom type
        class CustomId:
            def __init__(self, value: str):
                self.value = value

        # Create converter with custom type
        converter = FunctionSchemaConverter()
        converter.type_registry.register(
            CustomId,
            lambda: {
                "type": "string",
                "pattern": "^[A-Z]{2}\\d{6}$",
                "description": "Custom ID format: 2 uppercase letters followed by 6 digits"
            }
        )

        # Test function with custom type
        def process_custom_id(
            id: CustomId,
            name: str
        ) -> Dict[str, Any]:
            """Process data with custom ID type."""
            pass

        schema = converter.convert(process_custom_id)
        print("\nSchema for custom type:")
        print(json.dumps(schema, indent=2, ensure_ascii=False, cls=SchemaEncoder))

    except Exception as e:
        print(f"Error testing custom type: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()