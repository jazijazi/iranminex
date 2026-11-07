import re
import ipaddress
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address

def validate_ip_whitelist(value):
    """
    Validates a comma-separated list of IPs and/or CIDR ranges.
    Accepts: 192.168.1.10, 192.168.1.0/24, 2001:db8::/32, etc.
    """
    if not value:
        return
    entries = [v.strip() for v in value.split(",") if v.strip()]
    for entry in entries:
        try:
            # strict=False allows "192.168.1.5/24" (host bits set) too
            ipaddress.ip_network(entry, strict=False)
        except ValueError:
            raise ValidationError(
                f"{entry} یک ip یا رنج ip معتبر نیست"
            )

class CustomPasswordValidator:
    """
    Custom password validator with configurable requirements.
    ! set AUTH_PASSWORD_VALIDATORS in setting file 
    """
    def __init__(self, min_length=8, require_uppercase=True, require_lowercase=True, 
                 require_numbers=True, require_special_chars=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_numbers = require_numbers
        self.require_special_chars = require_special_chars
    
    def validate(self, password, user=None):
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"طول رمزعبور حداقل {self.min_length} باشد")
        
        if self.require_uppercase and not any(char.isupper() for char in password):
            errors.append("رمزعبور باید شامل حروف بزرگ لاتین باشد")
        
        if self.require_lowercase and not any(char.islower() for char in password):
            errors.append("رمزعبور باید شامل حروف کوچک لاتین باشد")
        
        if self.require_numbers and not any(char.isdigit() for char in password):
            errors.append("رمزعبور باید شامل اعداد باشد")
        
        if self.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("رمزعبور باید شامل کاراکترهای خاص باشد")
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        help_text = "رمز عبور باید شامل:\n"
        help_text += f"- طول رمزعبور باید حداقل {self.min_length} باشد\n"
        
        if self.require_uppercase:
            help_text += "- حداقل یک حرف بزرگ لاتین\n"
        
        if self.require_lowercase:
            help_text += "- حداقل یک حرف کوچک لاتین\n"
        
        if self.require_numbers:
            help_text += "- حداقل یک عدد\n"
        
        if self.require_special_chars:
            help_text += "- حداقل یک کاراکتر خاص (!@#$%^&*(),.?\":{}|<>)\n"
        
        return help_text