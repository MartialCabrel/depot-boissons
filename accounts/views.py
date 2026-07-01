from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy


class ConnexionView(LoginView):
    template_name = 'accounts/login.html'


def deconnexion(request):
    logout(request)
    return redirect('login')