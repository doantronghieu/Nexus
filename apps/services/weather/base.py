"""
Base service class for weather API interactions.
"""
import httpx
from typing import Optional, Dict, Any
from .config import settings
from .exceptions import APIError, ServiceUnavailableError
from .logger import logger


class BaseWeatherService:
    """Base class for weather API services."""
    
    def __init__(self, base_url: str, timeout: Optional[int] = None):
        """
        Initialize the service.
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout or settings.REQUEST_TIMEOUT
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True
        )
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            headers: Request headers
        
        Returns:
            Dict[str, Any]: API response data
        
        Raises:
            APIError: If the API request fails
            ServiceUnavailableError: If the service is unavailable
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = headers or {}
        
        # Add API key if configured
        if settings.API_KEY:
            params = params or {}
            params['apikey'] = settings.API_KEY
        
        try:
            response = await self.client.request(
                method,
                url,
                params=params,
                json=data,
                headers=headers
            )
            
            logger.debug(f"API Request: {method} {url}")
            logger.debug(f"Params: {params}")
            logger.debug(f"Response Status: {response.status_code}")
            
            # Check for successful response
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            # Handle API errors
            error_detail = None
            try:
                error_detail = e.response.json()
            except Exception:
                pass
            
            raise APIError(
                f"API request failed: {str(e)}",
                status_code=e.response.status_code,
                detail=error_detail
            )
            
        except httpx.RequestError as e:
            # Handle connection/timeout errors
            raise ServiceUnavailableError(
                f"Service unavailable: {str(e)}",
                detail={"error_type": e.__class__.__name__}
            )
            
        except Exception as e:
            # Handle unexpected errors
            logger.exception("Unexpected error making API request")
            raise APIError(
                f"Unexpected error: {str(e)}",
                status_code=500
            )
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return await self._make_request("GET", endpoint, params=params)
    
    async def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return await self._make_request("POST", endpoint, params=params, data=data)