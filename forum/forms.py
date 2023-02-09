from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for adding comments to blog post
    """
    class Meta:
        model = Comment
        fields = ('body',)
