from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from .forms import LoginForm


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        return render(request, 'login/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            return redirect('/todo/')
        return render(request, 'login/login.html', {'form': form})
