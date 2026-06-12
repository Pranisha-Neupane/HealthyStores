from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            # rating is rendered as custom star inputs in the template
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Tell us about your experience...'}),
        }
