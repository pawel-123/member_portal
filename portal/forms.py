from django import forms

from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'product',
            'text',
        ]
        labels = {
            'product': 'Type of claim',
            'text': 'Your message',
        }
