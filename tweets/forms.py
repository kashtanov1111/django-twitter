from django import forms
from .models import Tweet
from django.utils import timezone
from datetime import datetime, timedelta


class TweetCreateForm(forms.ModelForm):
    #published = forms.DateTimeField(
    #    input_formats = ['%Y-%m-%dT%H:%M'],
    #    widget = forms.DateTimeInput(
    #        attrs={
    #            'type': 'datetime-local',
    #            'value': datetime.now().strftime("%Y-%m-%dT%H:%M")},
    #        format='%Y-%m-%dT%H:%M')
    #)
    def clean_published(self):
        a = self.cleaned_data['published']
        if a <= timezone.now() - timedelta(days=1):
            raise forms.ValidationError("You can't choose the date in the past")
        return a

    class Meta:
        model = Tweet
        fields = ('text', 'image', 'published')
        widgets = {
            #'published':forms.DateInput(attrs={'type':'date', 'value': datetime.now().strftime("%d-%m-%Y")}),
            'published':forms.DateTimeInput(attrs={'type':'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }