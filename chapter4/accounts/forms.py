from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ("username", "password", "remember_me")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "bio", "website", "profile_image")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
