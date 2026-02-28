from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'cover_image', 'category', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post Title'}),
            'body': forms.Textarea(attrs={'placeholder': 'Write your post here...', 'rows': 10}),
            'status': forms.Select(),
        }