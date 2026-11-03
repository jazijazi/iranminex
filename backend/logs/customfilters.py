import logging

class SafeExtraFieldsFilter(logging.Filter):
    """
        NEW FILTER (added to filter field in logConfig)
        this is used for adding extra fields to log from extra: field to add to formatter safely
    """
    def filter(self, record):
        # Add defaults if missing
        for field in ['ip', 'username', 'route', 'method']:
            if not hasattr(record, field):
                if field == 'ip':
                    setattr(record, field, '0.0.0.0')
                else:
                    setattr(record, field, '-')
        return True

class RequestInfoFilter(logging.Filter):
    """
    - Django's Built-in Logs: When Django detects security issues (CSRF, DisallowedHost, etc.), 
        it automatically creates log records that include a request attribute
    - This Filter's Job: Extract useful information from that
        request and add it as record attributes (record.ip, record.username, etc.)
    - Handler Usage: The DjangoDatabaseHandlerVerbose then reads these attributes and saves them to your database
    - Suggested Filter Chain:
        add_request_info → Extracts from Django's request
        add_safe_extras → Ensures safe defaults if extraction fails
    """
    def filter(self, record):
        try:
            request = getattr(record, 'request', None)
            if request:
                # More robust IP extraction
                r_ip = (request.META.get('HTTP_X_REAL_IP') or 
                       request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or
                       request.META.get('REMOTE_ADDR'))
                record.ip = r_ip or '0.0.0.0'
                
                user = getattr(request, 'user', None)
                if user and hasattr(user, 'is_authenticated'):
                    # Handle both callable and property is_authenticated
                    is_auth = user.is_authenticated() if callable(user.is_authenticated) else user.is_authenticated
                    if is_auth:
                        record.username = getattr(user, 'username', 'authenticated_user')
                    else:
                        record.username = 'anonymous'
                else:
                    record.username = 'anonymous'
                
                # Limit route length to prevent huge URLs
                route = request.path if hasattr(request, 'path') else '-'
                record.route = route[:100] if route else '-'  # Truncate long URLs
                
                record.method = request.method if hasattr(request, 'method') else '-'
            else:
                record.ip = '0.0.0.0'
                record.username = record.route = record.method = '-'
        except Exception:
            record.ip = '0.0.0.0'
            record.username = record.route = record.method = '-'
        return True