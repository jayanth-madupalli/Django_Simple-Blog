from django import forms
from .models import Comment


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'Post a comment', 'rows': 3, 'width': '100%'})
        }
