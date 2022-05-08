
from django import forms
from django.contrib.auth.forms import UserCreationForm

from tests.models import User


class CreationTestForm(UserCreationForm):
    name = forms.CharField(
        label='Название теста',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Введите название теста'
            }
        )
    )
    icon = forms.ImageField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Введите ваш адрес электронной почты'
            }
        )
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
