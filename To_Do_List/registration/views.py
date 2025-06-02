from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework.views import APIView
from .forms import RegistrationForm


class RegistrationView(APIView):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/todo/')
        return render(request, 'registration/registration.html', {'form': form})
