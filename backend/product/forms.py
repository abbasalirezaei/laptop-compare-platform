from django import forms
from .models import LaptopComment

class LaptopCommentForm(forms.ModelForm):
    class Meta:
        model = LaptopComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your comment...'})
        }