from django import forms

class LinkForm(forms.Form):
    youtube_url = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(attrs={'rows': 1, 'class': 'form-control', 'id': 'inputURL'})
    )