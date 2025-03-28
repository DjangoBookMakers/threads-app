from django import forms
from .models import Thread, Comment
from PIL import Image


def validate_image(image_file):
    """이미지 파일 유효성 검사"""
    try:
        img = Image.open(image_file)
        img.verify()  # 이미지 검증
        return True
    except:
        return False


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["content", "image"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "무슨 생각을 하고 계신가요?",
                    "class": "thread-textarea auto-resize",
                    "maxlength": 500,
                }
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # 파일 크기 제한 (5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("이미지 크기는 5MB 이하여야 합니다.")

            # 파일 형식 제한
            valid_extensions = ["jpg", "jpeg", "png", "gif"]
            ext = image.name.split(".")[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    "지원되는 이미지 형식은 JPG, JPEG, PNG, GIF입니다."
                )

            # 이미지 파일 검증
            if not validate_image(image):
                raise forms.ValidationError("유효하지 않은 이미지 파일입니다.")

        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "댓글을 입력하세요...",
                    "class": "auto-resize",
                    "maxlength": 200,
                }
            ),
        }
