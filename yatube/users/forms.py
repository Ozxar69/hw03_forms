from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ResetForm(PasswordResetForm):
    class Meta(PasswordResetForm):
        model = User
        fields = ('new_password', 'new_password_confirmation')
