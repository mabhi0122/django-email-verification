from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.forms import ValidationError


class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField(max_length=255, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exits.. Try again...')
        else:
              return email
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


    # def username_clean(self):
    #     username = self.cleaned_data.get('username')
    #     if not User.objects.filter(username = username).exists():
    #         raise ValidationError('The username you entered does not exist.')
    #     else:
    #         return username

    