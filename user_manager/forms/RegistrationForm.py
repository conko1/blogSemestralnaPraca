from django import forms
from user_manager.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Heslo')
    password_check = forms.CharField(widget=forms.PasswordInput, label='Zopakujte heslo')

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Meno',
            'email': 'E-Mail'
        }

    def clean_password_check(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password_check']:
            raise forms.ValidationError('Zadajte helsá, ktoré sa zhodujú')
        return form_data['password_check']
