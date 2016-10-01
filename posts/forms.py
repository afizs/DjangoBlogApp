from django import forms
from django.contrib.auth.models import User


from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish'
        ]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
