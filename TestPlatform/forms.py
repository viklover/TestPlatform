from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tests.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        # user.last_name = self.cleaned_data['last_name']
        # if commit and not User.objects.filter(nickname=user.nickname).exists():
        #     user.save()
        #     return True
        # return False
        return user


class EditUserForm(ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')

