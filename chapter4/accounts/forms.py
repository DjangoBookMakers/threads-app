from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text="필수. 유효한 이메일 주소를 입력하세요.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
