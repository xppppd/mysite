from django import forms
from .models import Comment,Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','excerpt','category','tags']