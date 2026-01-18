from django import forms
from .models import Post,Thread
from auth_system.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 3:
            raise forms.ValidationError("Слишком короткое сообщение (минимум 3 символа)")
        return content

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px;'}),
            'description': forms.Textarea(attrs={'rows': 4, 'style': 'width: 100%; padding: 8px;'}),
        }

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']
        labels = {
            'role': 'Выберите новую роль'
        }
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'})
        }