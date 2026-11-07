from rest_framework.request import Request
from typing import Optional
import ipaddress
from django.http import HttpRequest
def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False
    
def strip_port(ip: str) -> str:
    """
    Remove port from an IP string while preserving IPv6 addresses.

    Examples:
        1.2.3.4:8080      -> 1.2.3.4
        [::1]:8080        -> ::1
        2001:db8::1       -> 2001:db8::1
    """

    if ip.startswith('['):
        end = ip.find(']')
        if end != -1:
            return ip[1:end]

    # IPv4 with port has exactly one colon
    if ip.count(':') == 1:
        return ip.split(':')[0]

    return ip
    
def get_client_ip(request: Request | HttpRequest , trust_proxy: bool = True) -> Optional[str]:
    """
    Extract the client IP address from a Django REST Framework Request object.

    Args:
        request (Request): The DRF Request object
        trust_proxy (bool): Whether to trust proxy headers (default: True)
        
    Returns:
        Optional[str]: The client's IP address or None if not found
    """
    
    # Headers to check in order of preference (Nginx-friendly)
    proxy_headers = [
        'HTTP_CF_CONNECTING_IP',
        'HTTP_TRUE_CLIENT_IP',
        'HTTP_X_REAL_IP', 

        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED', 
        'HTTP_X_FORWARDED_FOR_IP',
        'HTTP_X_CLUSTER_CLIENT_IP',

        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
        'HTTP_X_COMING_FROM',
        'HTTP_PROXY_CLIENT_IP',
        'HTTP_WL_PROXY_CLIENT_IP',
        'HTTP_FASTLY_CLIENT_IP',
        'HTTP_AKAMAI_ORIGIN_HOP',

        'HTTP_CLIENT_IP',
        'HTTP_X_CLIENT_IP',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_ORIGINAL_FORWARDED_FOR', 

        'REMOTE_ADDR',
    ]
    
    if trust_proxy:
        # Check proxy headers first
        for header in proxy_headers:
            header_value = request.META.get(header)
            if not header_value:
                continue
                
            # Handle comma-separated IPs (chain of proxies)
            ips = [ip.strip() for ip in header_value.split(',')]
            
            for ip in ips:
                ip = strip_port(ip)
                if is_valid_ip(ip):
                    return ip
                
    # Fall back to direct connection IP
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr and is_valid_ip(remote_addr):
        print(f"Client IP from REMOTE_ADDR: {remote_addr}")
        return remote_addr
    
    # Last resort: check for any IP-like string in common headers
    fallback_headers = ['HTTP_CLIENT_IP', 'HTTP_X_COMING_FROM', 'HTTP_VIA']
    for header in fallback_headers:
        header_value = request.META.get(header)
        if header_value and is_valid_ip(header_value.strip()):
            print(f"Client IP found in fallback {header}: {header_value.strip()}")
            return header_value.strip()
    
    print("Could not determine client IP address")
    return None