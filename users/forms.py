from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "email",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    pass


class CustomChangeForm(UserChangeForm):
    pass