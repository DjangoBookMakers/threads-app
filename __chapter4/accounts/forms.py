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

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get("profile_image")
        if profile_image:
            # 파일 크기 제한 (5MB)
            if profile_image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("이미지 크기는 5MB 이하여야 합니다.")

            # 파일 형식 제한
            valid_extensions = ["jpg", "jpeg", "png", "gif"]
            ext = profile_image.name.split(".")[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    "지원되는 이미지 형식은 JPG, JPEG, PNG, GIF입니다."
                )

        return profile_image
