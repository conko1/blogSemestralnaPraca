from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Užívateľské meno', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Heslo', required=True)
