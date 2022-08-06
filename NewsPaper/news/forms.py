from django import forms
from django.core.exceptions import ValidationError


from .models import Post


class PostForm(forms.ModelForm):
    text = forms.Textarea()
    title = forms.CharField(max_length=40)

    class Meta:
        model = Post

        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст поста не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "Название не должно совпадать с основным текстом."
            )
        return cleaned_data

