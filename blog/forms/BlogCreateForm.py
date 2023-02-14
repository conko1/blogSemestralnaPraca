from django import forms


class BlogCreateForm(forms.Form):
    title = forms.CharField(label='Názov blogu', required=True, max_length=250)
    content = forms.CharField(label='Obsah blogu', required=True, widget=forms.Textarea)
