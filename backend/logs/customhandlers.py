import logging
from datetime import datetime
import logging.handlers


class DatabaseHandler(logging.Handler):
    def emit(self, record):
        from logs.models import Logs #must be here !

        # read record property names from formmater !
        # this is simple formmater ( not include ip/method/ etc. )
        try:
            log_entry = Logs.objects.create(
                writer = 'django',
                tarikh = datetime.fromtimestamp(record.created),
                level = record.levelname.upper(),
                massage = record.getMessage(),
            )
            log_entry.save()
        except Exception:
            self.handleError(record)

class DatabaseHandlerVerbose(logging.Handler):
    def emit(self, record):
        from logs.models import Logs #must be here !

        # read record property names from formmater !
        # this in include (ip,method,path,username)
        # make sure add_safe_extras filter is inculded to handler filed in logConfig file 
        try:
            log_entry = Logs.objects.create(
                username = record.username,
                writer = 'manual',
                tarikh = datetime.fromtimestamp(record.created),
                level = record.levelname.upper(),
                ip = record.ip,
                method = record.method,
                route = record.route,
                massage = record.getMessage(),
            )
            log_entry.save()
        except Exception:
            self.handleError(record)

class DjangoDatabaseHandler(logging.Handler):
    """
        Whenever Django needs to send a log, it should do so to the database.
        this is simple formmater ( not include ip/method/ etc. )
    """
    def emit(self, record):
        from logs.models import Logs
        # read record property names from formmater !
        try:
            log_entry = Logs.objects.create(
                writer = 'django',
                tarikh = datetime.fromtimestamp(record.created),
                level = record.levelname.upper(),
                massage = record.getMessage(),
            )
            log_entry.save()
        except Exception:
            self.handleError(record)

class DjangoDatabaseHandlerVerbose(logging.Handler):
    """
        Whenever Django needs to send a log, it should do so to the database.
        this handler get ip/username/method/path 
        so make sure SafeExtraFieldsFilter be included in filters
    """
    def emit(self, record):
        from logs.models import Logs
        # read record property names from formmater !
        try:
            log_entry = Logs.objects.create(
                username = record.username,
                writer = 'manual',
                tarikh = datetime.fromtimestamp(record.created),
                level = record.levelname.upper(),
                ip = record.ip,
                method = record.method,
                route = record.route,
                massage = record.getMessage(),
            )
            log_entry.save()
        except Exception:
            self.handleError(record)