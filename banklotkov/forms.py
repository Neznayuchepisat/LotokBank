from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile, BalanceRequest, Loan, Review, Product


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Имя пользователя"), max_length=254)
    password = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput)


class BalanceRequestForm(forms.ModelForm):
    class Meta:
        model = BalanceRequest
        fields = ['amount']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'term']


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, 
        required=False, 
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False, 
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False, 
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'birth_date']
        labels = {
            'phone': 'Телефон',
            'avatar': 'Фото профиля',
            'birth_date': 'Дата рождения'
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)
        user.save()
        return profile


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите ваш отзыв'
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5
            })
        }
        labels = {
            'text': 'Отзыв',
            'rating': 'Рейтинг (1-5)'
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'amount', 'price', 'availible']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Название товара'
                },
            ), 
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Описание товара',
                    'rows': 3
                },
            ), 
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'min': 0
                }
            ), 
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'step': '0.01', 
                    'min': 0
                }
            ), 
            'availible': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }