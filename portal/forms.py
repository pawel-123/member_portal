from django import forms

from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'product',
            'text',
            'attachment',
        ]
        labels = {
            'product': 'Type of claim',
            'text': 'Your message',
            'attachment': 'Your medical file',
        }
