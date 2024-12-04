from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from account.models import Profile
from order.models import Order



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'street', 'gender']








class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
        attrs={
            'autocomplete': 'text',
            'placeholder': 'Введите логин',
        }
        
    ),
    required=False,
    validators=[RegexValidator(r'[^0-9а-яА-ЯёЁ]', "Введите логин латиницей")]
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
        attrs={
            'autocomplete': 'email',
            'placeholder': 'Введите почту',
        }
        ),
        required=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            'placeholder': 'Введите пароль',
            }
        ),
        required=-False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            'placeholder': 'Повторите пароль',
            }
        ),
        required=False
        
    )
    
    # def clean_password1(self):
    #     password = self.cleaned_data['password1']
    #     if password == '':
    #         raise forms.ValidationError('Введите пароль', code='invalid')
    #     return password
    
    # def clean_password1(self):
    #     password = self.cleaned_data['username']
    #     if password == '':
    #         raise forms.ValidationError('Введите логин', code='invalid')
    #     return password
    
    # def clean_password1(self):
    #     password = self.cleaned_data['email']
    #     if password == '':
    #         raise forms.ValidationError('Введите электронную почту', code='invalid')
    #     return password
    
    # class Meta(UserCreationForm.Meta):
    #     fields = ("username", "email")



class LoginForm(AuthenticationForm):
    username = forms.CharField( 
    max_length=254,
    widget=forms.TextInput(
        attrs={
            'autocomplete': 'text',
            'placeholder': 'логин', 
        }
    ),
    required=False
)
    
password = forms.CharField(
    widget=forms.PasswordInput(
        attrs={
            "autocomplete": "current-password",
            'placeholder': 'Пароль',
        }
    ),
    required=False
)
    
error_messages = {
        "invalid_login": (
            "Введите логин и пароль правильно"
        ),
    }
    
def clean_password(self):
        password = self.cleaned_data['password']
        if password == '':
            raise forms.ValidationError('Введите пароль', code='invalid')
        return password
def clean_username(self):
        username = self.cleaned_data['username']
        if username == '':
            raise forms.ValidationError('Введите логин', code='invalid')
        if not User.objects.filter(username=username):
            raise forms.ValidationError('Такого пользователя не существует', code='invalid')
        return username


        
    
    
   