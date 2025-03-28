from django import forms
from .models import Thread


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
