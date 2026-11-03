from django import forms
from django.contrib.auth.hashers import make_password , identify_hasher
from django.contrib.auth import get_user_model

User = get_user_model()

def is_hashed_password(value: str) -> bool:
    """
    Return True if `value` looks like a valid Django hashed password.
    identify_hasher() raises an exception for non-hashed strings.
    """
    if not value:
        return False
    try:
        identify_hasher(value)
        return True
    except Exception:
        return False
    
class UserAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="PASSWORD",
        widget=forms.TextInput(
            attrs={
                "style": (
                    "width: 400px; "
                    "padding: 6px 8px; "
                    "border-radius: 6px; "
                    "border: 2px solid #0E1799; "
                    "font-family: tahoma; "
                ),
                "placeholder": "رمز عبور جدید را وارد کنید (در صورت نیاز)",
            }
        ),
        required=False,
        help_text=(
            '<span style="color:#d9534f; font-size:13px;">'
            '⚠️ اگر قصد تغییر رمز عبور دارید، مقدار جدید را وارد کنید. '
            'در غیر این صورت این فیلد را تغییر ندهید.'
            '</span>'
            '<br/>'
            '<span style="color:#d9534f; font-size:13px;">'
            '⚠️ از ورود پسورد جدید به صورت هش شده خودداری کنید '
            '</span>'
        ),
    )
    
    class Meta:
        model = User
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the original password hash
        if self.instance and self.instance.pk:
            self._original_password = self.instance.password
            # Clear the password field in the form (don't show the hash)
            self.fields['password'].initial = ''
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Editing an existing user
        if self.instance and self.instance.pk:
            # 1) If left blank -> keep current password
            if not password:
                return self.instance.password

            # 2) If posted value is EXACTLY the stored hash -> keep as-is (no re-hash)
            if password == self.instance.password:
                return password

            # 3) If the posted value is already a valid hash (some edge-case paste) -> keep it
            if is_hashed_password(password):
                return password

            # 4) Otherwise it's plain text -> hash it
            return make_password(password)

        # Creating a new user
        if password:
            if is_hashed_password(password):
                return password
            return make_password(password)

        return password