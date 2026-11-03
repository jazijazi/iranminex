import logging
from typing import Dict, Union, Optional, TypedDict
from rest_framework.request import Request
from django.http import HttpRequest
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser


class RequestDetails(TypedDict):
    """Type definition for request details dictionary"""
    username: str
    ip: str
    route: str
    method: str


def get_details_from_request(
    request: Union[Request, HttpRequest]
) -> RequestDetails:
    """
    Extract details from a Django/DRF request object.
    
    Args:
        request: Django HttpRequest or DRF Request object
        
    Returns:
        RequestDetails: Dictionary containing username, ip, route, and method
        
    Raises:
        AttributeError: If request object doesn't have required attributes
        TypeError: If request is not a valid request object
    """
    if not hasattr(request, 'META'):
        raise TypeError("Invalid request object: missing META attribute")
    
    # Extract username with proper type checking
    username: str = _extract_username(request)
    
    # Extract IP address with fallback chain
    ip: str = _extract_ip_address(request)
    
    # Extract route/path with fallbacks
    route: str = _extract_route(request)
    
    # Extract HTTP method
    method: str = _extract_method(request)
    
    return RequestDetails(
        username=username,
        ip=ip,
        route=route,
        method=method
    )


def _extract_username(request: Union[Request, HttpRequest]) -> str:
    """Extract username from request with proper type checking."""
    try:
        user: Union[AbstractBaseUser, AnonymousUser, None] = getattr(request, 'user', None)
        
        if user is None:
            return "Anonymous"
            
        # Check if user is authenticated
        if hasattr(user, 'is_authenticated') and callable(user.is_authenticated):
            is_auth: bool = user.is_authenticated()
        elif hasattr(user, 'is_authenticated'):
            is_auth: bool = bool(user.is_authenticated)
        else:
            return "Anonymous"
            
        if is_auth and hasattr(user, 'username'):
            username: Optional[str] = getattr(user, 'username', None)
            return str(username) if username else "AuthenticatedUser"
        
        return "Anonymous"
        
    except Exception as e:
        logging.warning(f"Error extracting username: {e}")
        return "Anonymous"


def _extract_ip_address(request: Union[Request, HttpRequest]) -> str:
    """Extract IP address from request META with multiple fallbacks."""
    try:
        meta: Dict[str, str] = getattr(request, 'META', {})
        
        # Priority order for IP extraction
        ip_headers = [
            'HTTP_CF_CONNECTING_IP', # Cloudflare's real client IP (most reliable)
            'HTTP_X_REAL_IP', # Set by nginx from X-Real-IP
            'HTTP_X_FORWARDED_FOR', # Standard proxy header
            'HTTP_X_FORWARDED',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_CLIENT_IP',
            'REMOTE_ADDR'
        ]
        
        for header in ip_headers:
            ip: Optional[str] = meta.get(header)
            if ip:
                # Handle comma-separated IPs (X-Forwarded-For can have multiple)
                ip = ip.split(',')[0].strip()
                if ip and ip != 'unknown':
                    return str(ip)
        
        return '0.0.0.0'
        
    except Exception as e:
        logging.warning(f"Error extracting IP address: {e}")
        return '0.0.0.0'


def _extract_route(request: Union[Request, HttpRequest]) -> str:
    """Extract route/path from request with fallbacks."""
    try:
        # Try path_info first (more reliable)
        if hasattr(request, 'path_info'):
            path: Optional[str] = getattr(request, 'path_info', None)
            if path:
                return str(path)
        
        # Fallback to path
        if hasattr(request, 'path'):
            path = getattr(request, 'path', None)
            if path:
                return str(path)
        
        # Last resort - try to get from META
        meta: Dict[str, str] = getattr(request, 'META', {})
        path = meta.get('PATH_INFO', meta.get('REQUEST_URI', '/'))
        return str(path)
        
    except Exception as e:
        logging.warning(f"Error extracting route: {e}")
        return '/'


def _extract_method(request: Union[Request, HttpRequest]) -> str:
    """Extract HTTP method from request."""
    try:
        method: Optional[str] = getattr(request, 'method', None)
        if method:
            return str(method).upper()
        
        # Fallback to META
        meta: Dict[str, str] = getattr(request, 'META', {})
        method = meta.get('REQUEST_METHOD', 'GET')
        return str(method).upper()
        
    except Exception as e:
        logging.warning(f"Error extracting method: {e}")
        return 'GET'