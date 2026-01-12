from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите варианты ответов с новой строки.'
        }),
        label="Варианты ответов",
        help_text="Каждый вариант с новой строки"
    )

    class Meta:
        model = Question
        fields = ["title", "content", "status"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема опроса'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }