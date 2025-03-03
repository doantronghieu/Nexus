"""
Utility functions for the Weather Service.
"""
from datetime import datetime, timezone
from typing import Union, Dict, Any, Optional
from .exceptions import ValidationError


def validate_date_range(
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> tuple[Optional[datetime], Optional[datetime]]:
    """
    Validate and convert date range parameters.
    
    Args:
        start_date: Start date string or datetime
        end_date: End date string or datetime
    
    Returns:
        tuple: Validated start and end datetimes
    
    Raises:
        ValidationError: If date validation fails
    """
    try:
        # Convert string dates to datetime if necessary
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Validate date range if both dates are provided
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date must be before end date")
        
        return start_date, end_date
        
    except ValueError as e:
        raise ValidationError(f"Invalid date format: {str(e)}")


def format_date(dt: datetime) -> str:
    """
    Format datetime to ISO 8601 string.
    
    Args:
        dt: Datetime to format
    
    Returns:
        str: Formatted date string
    """
    return dt.isoformat()


def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Validate geographic coordinates.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Raises:
        ValidationError: If coordinates are invalid
    """
    if not -90 <= latitude <= 90:
        raise ValidationError("Latitude must be between -90 and 90 degrees")
    if not -180 <= longitude <= 180:
        raise ValidationError("Longitude must be between -180 and 180 degrees")


def clean_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove None values from dictionary.
    
    Args:
        data: Dictionary to clean
    
    Returns:
        Dict[str, Any]: Cleaned dictionary
    """
    return {k: v for k, v in data.items() if v is not None}


def get_utc_now() -> datetime:
    """
    Get current UTC datetime.
    
    Returns:
        datetime: Current UTC datetime
    """
    return datetime.now(timezone.utc)