from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_youtubeURL(url):
    if not url.startswith("https://www.youtube.com/watch?v="):
        raise ValidationError(_("%(url)s is not a valid YouTube URL"), params={"url": url},)

class LinkForm(forms.Form):
    youtube_url = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(attrs={'rows': 1, 'class': 'form-control', 'id': 'inputURL'}),
        validators=[validate_youtubeURL]
    )