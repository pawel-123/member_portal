from django import forms
from multiupload.fields import MultiFileField

from .models import Claim, ClaimAttachment

class NewClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['product', 'text']

    files = MultiFileField(min_num=1, max_num=5, max_file_size=1024*1024*10)

    def save(self, commit=True):
        instance = super(NewClaimForm, self).save(commit)
        for each in self.cleaned_data['files']:
            ClaimAttachment.objects.create(attachment=each, claim=instance)

        return instance
