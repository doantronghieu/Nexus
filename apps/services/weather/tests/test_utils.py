"""
Tests for Weather Service utility functions.
"""
import pytest
from datetime import datetime, timezone

from ..utils import (
    validate_date_range,
    format_date,
    validate_coordinates,
    clean_none_values,
    get_utc_now
)
from ..exceptions import ValidationError


class TestValidateDateRange:
    """Test cases for date range validation."""
    
    def test_valid_date_strings(self):
        """Test validation of valid date strings."""
        start_date = "2024-01-01"
        end_date = "2024-01-07"
        
        result_start, result_end = validate_date_range(start_date, end_date)
        
        assert isinstance(result_start, datetime)
        assert isinstance(result_end, datetime)
        assert result_start.year == 2024
        assert result_end.year == 2024
        assert result_start.month == 1
        assert result_start.day == 1
    
    def test_valid_datetime_objects(self):
        """Test validation of datetime objects."""
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 7)
        
        result_start, result_end = validate_date_range(start_date, end_date)
        
        assert result_start == start_date
        assert result_end == end_date
    
    def test_invalid_date_order(self):
        """Test validation of invalid date order."""
        start_date = "2024-01-07"
        end_date = "2024-01-01"
        
        with pytest.raises(ValidationError) as exc_info:
            validate_date_range(start_date, end_date)
        assert "Start date must be before end date" in str(exc_info.value)
    
    def test_invalid_date_format(self):
        """Test validation of invalid date format."""
        with pytest.raises(ValidationError) as exc_info:
            validate_date_range("2024/01/01", "2024/01/07")
        assert "Invalid date format" in str(exc_info.value)
    
    def test_optional_dates(self):
        """Test validation with optional dates."""
        result_start, result_end = validate_date_range()
        assert result_start is None
        assert result_end is None
    
    def test_single_date(self):
        """Test validation with only start date."""
        start_date = "2024-01-01"
        result_start, result_end = validate_date_range(start_date)
        assert isinstance(result_start, datetime)
        assert result_end is None
    
    def test_timezone_handling(self):
        """Test handling of dates with timezone information."""
        start_date = "2024-01-01T00:00:00Z"
        end_date = "2024-01-07T00:00:00Z"
        
        result_start, result_end = validate_date_range(start_date, end_date)
        
        assert result_start.tzinfo is not None
        assert result_end.tzinfo is not None


class TestFormatDate:
    """Test cases for date formatting."""
    
    def test_format_date_with_timezone(self):
        """Test date formatting with timezone."""
        dt = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        formatted = format_date(dt)
        assert formatted == "2024-01-01T12:00:00+00:00"
    
    def test_format_date_without_timezone(self):
        """Test date formatting without timezone."""
        dt = datetime(2024, 1, 1, 12, 0)
        formatted = format_date(dt)
        assert formatted == "2024-01-01T12:00:00"
    
    def test_format_date_microseconds(self):
        """Test date formatting with microseconds."""
        dt = datetime(2024, 1, 1, 12, 0, 0, 123456, tzinfo=timezone.utc)
        formatted = format_date(dt)
        assert formatted == "2024-01-01T12:00:00.123456+00:00"


class TestValidateCoordinates:
    """Test cases for coordinate validation."""
    
    def test_valid_coordinates(self):
        """Test validation of valid coordinates."""
        validate_coordinates(0, 0)  # Equator
        validate_coordinates(90, 180)  # North pole, east limit
        validate_coordinates(-90, -180)  # South pole, west limit
        validate_coordinates(45.5, -120.5)  # Decimal coordinates
    
    def test_invalid_latitude(self):
        """Test validation of invalid latitude."""
        with pytest.raises(ValidationError) as exc_info:
            validate_coordinates(91, 0)
        assert "Latitude must be between -90 and 90 degrees" in str(exc_info.value)
        
        with pytest.raises(ValidationError):
            validate_coordinates(-91, 0)
    
    def test_invalid_longitude(self):
        """Test validation of invalid longitude."""
        with pytest.raises(ValidationError) as exc_info:
            validate_coordinates(0, 181)
        assert "Longitude must be between -180 and 180 degrees" in str(exc_info.value)
        
        with pytest.raises(ValidationError):
            validate_coordinates(0, -181)
    
    def test_extreme_values(self):
        """Test validation of extreme coordinate values."""
        validate_coordinates(-90, -180)  # Minimum values
        validate_coordinates(90, 180)  # Maximum values
        
        with pytest.raises(ValidationError):
            validate_coordinates(90.000001, 0)
        with pytest.raises(ValidationError):
            validate_coordinates(0, 180.000001)


class TestCleanNoneValues:
    """Test cases for cleaning None values from dictionaries."""
    
    def test_clean_none_values(self):
        """Test cleaning None values from dictionary."""
        data = {
            "a": 1,
            "b": None,
            "c": "test",
            "d": None,
            "e": 0,
            "f": False,
            "g": "",
        }
        
        cleaned = clean_none_values(data)
        
        assert "b" not in cleaned
        assert "d" not in cleaned
        assert cleaned["a"] == 1
        assert cleaned["c"] == "test"
        assert cleaned["e"] == 0
        assert cleaned["f"] is False
        assert cleaned["g"] == ""
    
    def test_clean_empty_dict(self):
        """Test cleaning an empty dictionary."""
        assert clean_none_values({}) == {}
    
    def test_clean_no_none_values(self):
        """Test cleaning dictionary with no None values."""
        data = {"a": 1, "b": "test"}
        assert clean_none_values(data) == data
    
    def test_clean_nested_dict(self):
        """Test cleaning nested dictionary."""
        data = {
            "a": {"x": 1, "y": None},
            "b": None,
            "c": {"p": None, "q": 2}
        }
        cleaned = clean_none_values(data)
        assert "b" not in cleaned
        assert cleaned["a"]["x"] == 1
        assert "y" not in cleaned["a"]
        assert "p" not in cleaned["c"]
        assert cleaned["c"]["q"] == 2


class TestGetUtcNow:
    """Test cases for getting current UTC time."""
    
    def test_get_utc_now(self):
        """Test getting current UTC time."""
        now = get_utc_now()
        
        assert isinstance(now, datetime)
        assert now.tzinfo == timezone.utc
        
        # Test that the time is recent (within last second)
        time_diff = datetime.now(timezone.utc) - now
        assert time_diff.total_seconds() < 1