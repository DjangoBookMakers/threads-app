from django import forms
from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["content", "image"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "무슨 생각을 하고 계신가요?"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "댓글을 입력하세요..."}
            ),
        }
