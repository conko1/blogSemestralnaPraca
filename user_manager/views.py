from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect, render

from .forms.LoginForm import LoginForm
from .forms.RegistrationForm import RegisterForm


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


class LoginView(generic.FormView):
    template_name = 'user_manager/login_form.html'
    form_class = LoginForm
    success_url = '/blog/'

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = authenticate(self.request, username=form_data['username'], password=form_data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super().form_valid(form)
            else:
                return render(self.request, 'user_manager/login_form.html', {'error_message': 'Účet nie je aktívny'})
        else:
            return render(self.request, 'user_manager/login_form.html', {'error_message': 'Zadali ste nesprávne prihlasovacie údaje'})


class RegisterView(generic.FormView):
    template_name = 'user_manager/register_form.html'
    form_class = RegisterForm
    success_url = '/blog/'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
