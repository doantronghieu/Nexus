"""
Tests for Weather Service base service class.
"""
import pytest
import httpx
from unittest.mock import Mock, patch

from ..base import BaseWeatherService
from ..config import settings
from ..exceptions import APIError, ServiceUnavailableError


class TestBaseWeatherService:
    """Test cases for BaseWeatherService."""
    
    @pytest.fixture
    def base_service(self):
        """Create a test instance of BaseWeatherService."""
        return BaseWeatherService("https://api.test.com")
    
    @pytest.mark.asyncio
    async def test_make_request_success(self, base_service):
        """Test successful API request."""
        test_response = {"test": "data"}
        
        # Mock the httpx client response
        mock_response = Mock()
        mock_response.json.return_value = test_response
        mock_response.raise_for_status = Mock()
        
        with patch.object(base_service.client, 'request', return_value=mock_response):
            response = await base_service._make_request(
                "GET",
                "test",
                params={"param": "value"}
            )
            
            assert response == test_response
    
    @pytest.mark.asyncio
    async def test_make_request_api_error(self, base_service):
        """Test API error handling."""
        # Mock HTTP error response
        error_response = Mock()
        error_response.status_code = 400
        error_response.json.return_value = {"error": "Bad Request"}
        
        with patch.object(base_service.client, 'request') as mock_request:
            mock_request.side_effect = httpx.HTTPStatusError(
                "400 Bad Request",
                request=Mock(),
                response=error_response
            )
            
            with pytest.raises(APIError) as exc_info:
                await base_service._make_request("GET", "test")
            
            assert exc_info.value.status_code == 400
    
    @pytest.mark.asyncio
    async def test_make_request_service_unavailable(self, base_service):
        """Test service unavailable error handling."""
        with patch.object(base_service.client, 'request') as mock_request:
            mock_request.side_effect = httpx.RequestError("Connection failed")
            
            with pytest.raises(ServiceUnavailableError) as exc_info:
                await base_service._make_request("GET", "test")
            
            assert "Connection failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_request(self, base_service):
        """Test GET request method."""
        test_response = {"test": "data"}
        
        # Mock the _make_request method
        with patch.object(base_service, '_make_request', return_value=test_response):
            response = await base_service.get(
                "test",
                params={"param": "value"}
            )
            
            assert response == test_response
    
    @pytest.mark.asyncio
    async def test_post_request(self, base_service):
        """Test POST request method."""
        test_response = {"test": "data"}
        test_data = {"data": "test"}
        
        # Mock the _make_request method
        with patch.object(base_service, '_make_request', return_value=test_response):
            response = await base_service.post(
                "test",
                data=test_data,
                params={"param": "value"}
            )
            
            assert response == test_response
    
    @pytest.mark.asyncio
    async def test_api_key_inclusion(self, base_service):
        """Test API key inclusion in requests when configured."""
        test_response = {"test": "data"}
        test_api_key = "test_key"
        
        # Temporarily set API key
        original_api_key = settings.API_KEY
        settings.API_KEY = test_api_key
        
        try:
            # Mock the httpx client response
            mock_response = Mock()
            mock_response.json.return_value = test_response
            mock_response.raise_for_status = Mock()
            
            with patch.object(base_service.client, 'request') as mock_request:
                mock_request.return_value = mock_response
                
                await base_service._make_request("GET", "test")
                
                # Verify API key was included in request params
                call_args = mock_request.call_args
                assert call_args[1]['params']['apikey'] == test_api_key
                
        finally:
            # Restore original API key setting
            settings.API_KEY = original_api_key
    
    @pytest.mark.asyncio
    async def test_close(self, base_service):
        """Test client cleanup on close."""
        with patch.object(base_service.client, 'aclose') as mock_aclose:
            await base_service.close()
            mock_aclose.assert_called_once()