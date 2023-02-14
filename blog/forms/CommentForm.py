from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(
        label='Pridajte komentár',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}),
        max_length=500,
        required=True
    )
