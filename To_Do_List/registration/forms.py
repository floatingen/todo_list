from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(f'Пароли не совпадают')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} уже существует.')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password']
