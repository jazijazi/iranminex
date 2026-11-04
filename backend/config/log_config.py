import os
import logging
from decouple import config
from django.conf import settings

def ensure_log_directories():
    """Create log directories if they don't exist"""
    try:
        # Create main logs directory
        if not os.path.exists(settings.LOGS_ROOT):
            os.makedirs(settings.LOGS_ROOT, exist_ok=True)
            print(f"Created main logs directory: {settings.LOGS_ROOT}")
        
        # Create subdirectories
        subdirs = ['manual', 'django']
        for subdir in subdirs:
            dir_path = os.path.join(settings.LOGS_ROOT, subdir)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                print(f"Created log directory: {dir_path}")
                
    except Exception as e:
        print(f"Error creating log directories: {e}")
        raise

ENABLE_LOGGING = config('ENABLE_LOGGING', default=False, cast=bool)

"""
LOG LEVELs:
DEBUG (10)
INFO (20)
WARNING (30)
ERROR (40)
CRITICAL (50)
"""

if ENABLE_LOGGING:
    print("**** CUSTOM LOGGING IS ENABLED ****")

    # Ensure log directories exist before configuring handlers
    ensure_log_directories()

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {asctime} {message}",
                "style": "{",
            },
            "console": {
                "format": "{levelname} {asctime} {name} {message}",
                "style": "{",
            },
            "verbose_database": {
                "format": "{levelname} {asctime} {username} {ip} {method} {route} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "very_verbose": {
                "format": "{levelname} {asctime} {username} {ip} {method} {route} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            'sms_format': {
                "format": "{levelname} {asctime} {message}",
                "style": "{",
            },
        },

        'filters': {
            'only_info': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': lambda record: record.levelno == logging.INFO,
            },
            'only_warning_and_above': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': lambda record: record.levelno >= logging.WARNING,
            },
            'add_safe_extras': {
                '()': 'logs.customfilters.SafeExtraFieldsFilter',
            },
            'add_request_info': {
                '()': 'logs.customfilters.RequestInfoFilter',
            },
        },
        
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
            'console_errors': {
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },

            # MANUAL/CUSTOM HANDLERS
            'custom_database_handler': {
                'level': 'WARNING',
                'class': 'logs.customhandlers.DatabaseHandlerVerbose',
                'formatter': "verbose_database",
                'filters': ['add_safe_extras'],
            },
            'custom_problem_file_time': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'manual', 'manual_log_problem.log'),
                'when': 'D',
                'interval': 7,
                'backupCount': 12,
                'formatter': 'very_verbose',
                'filters': ['add_safe_extras'],
            },
            'custom_activity_file_time': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'manual', 'manual_log_activity.log'),
                'when': 'D',
                'interval': 3,
                'backupCount': 20,
                'formatter': 'very_verbose',
                'filters': ['only_info', 'add_safe_extras'],
            },
            'delete_activity_file_time': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'manual', 'delete_activity.log'),
                'when': 'W6', # Sunday
                'interval': 4, # Every 4 weeks (~monthly)
                'backupCount': 24, # Keep 2 years
                'formatter': 'very_verbose',
                'filters': ['add_safe_extras'],
            },
            'user_activity_file_time': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'manual', 'user_activity.log'),
                'when': 'W6', # Sunday
                'interval': 2, # Every 2 weeks
                'backupCount': 24, # Keep 2 years
                'formatter': 'very_verbose',
                'filters': ['only_info','add_safe_extras'],
            },
            'user_problem_file_time': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'manual', 'user_problem_activity.log'),
                'when': 'W6', # Sunday
                'interval': 2, # Every 2 weeks
                'backupCount': 48, # Keep 2 years
                'formatter': 'very_verbose',
                'filters': ['add_safe_extras'],
            },
            'sms_file_time':{
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'manual', 'sms_log_activity.log'),
                'when': 'D',
                'interval': 10,
                'backupCount': 20, 
                'formatter': 'sms_format',
                'filters': [],
            },
            
            # DJANGO FRAMEWORK HANDLERS
            "django_logs_itself_to_database": {
                'level': 'ERROR',
                'class': 'logs.customhandlers.DjangoDatabaseHandler',
                'formatter': "verbose",
            },
            "django_logs_itself_to_database_verbose": {
                'level': 'ERROR',
                'class': 'logs.customhandlers.DjangoDatabaseHandlerVerbose',
                'formatter': "very_verbose",
                'filters': ['add_request_info', 'add_safe_extras'],
            },
            'django_problem_file_time': {
                'level': 'WARNING',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'django', 'django_problem.log'),
                'when': 'D',
                'interval': 7,
                'backupCount': 8,
                'formatter': 'verbose',
            },
            'django_activity_file_time': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(settings.LOGS_ROOT, 'django', 'django_activity.log'),
                'when': 'D',
                'interval': 3,
                'backupCount': 10,
                'formatter': 'verbose',
                'filters': ['only_info'],
            },
        },

        'loggers': {
            # CUSTOM LOGGERS
            'custom_database_logger': {
                'handlers': ['custom_database_handler', 'console_errors'],  # Console for visibility
                'level': 'WARNING',
                'propagate': True,
            },
            'custom_file_logger': {
                'handlers': ['custom_problem_file_time', 'custom_activity_file_time', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
            'api_activity_logger':{
                'handlers': ['custom_problem_file_time', 'custom_activity_file_time','custom_database_handler', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
            'delete_activity_logger': {
                'handlers': ['delete_activity_file_time', 'custom_database_handler', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
            'user_activity_logger': {
                'handlers': ['user_activity_file_time', 'user_problem_file_time', 'custom_database_handler', 'console'],
                'level': 'INFO',
                'propagate': True,
            },

            # DJANGO BUILT-IN LOGGERS
            "django.security.DisallowedHost": {
                "handlers": ["django_logs_itself_to_database_verbose", "console_errors"],
                'level': 'WARNING',
                "propagate": False,
            },
            "django.security.csrf": {
                "handlers": ["django_logs_itself_to_database_verbose", "console_errors"],
                'level': 'WARNING',
                "propagate": False,
            },
            "django.security.SuspiciousOperation": {
                "handlers": ["django_logs_itself_to_database_verbose", "console_errors"],
                'level': 'WARNING',
                "propagate": False,
            },
            'django.request': {
                'handlers': ['django_problem_file_time', 'console_errors'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'ERROR',  # Only show DB errors, not all queries
                'propagate': False,
            },
            'django': {
                'handlers': ['django_problem_file_time', 'django_activity_file_time', 'console'],
                'level': 'INFO',
                'propagate': False,
            },
        },

        # ROOT LOGGER (important for third-party packages)
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    }
else:
    print("**** CUSTOM LOGGING IS DISABLED ****")
    # Fallback to basic console logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '{levelname} {asctime} {name} {message}',
                'style': '{',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': 'INFO',
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            }
        }
    }


"""
Usage Examples:

# Custom logging in views
import logging
custom_logger = logging.getLogger('custom_file_logger')
custom_logger.info('User action performed', extra={'ip': request.META.get('REMOTE_ADDR'), 'username': request.user.username})

# Database logging
db_logger = logging.getLogger('custom_database_logger')
db_logger.warning('Important event occurred', extra={'ip': '127.0.0.1', 'username': 'admin'})

"""