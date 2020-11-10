from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.hashers import check_password

from jobs.models import Skill
from jobs.forms import top_skills

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError(f'Пользователь с почтой {email} не зарегистрирован')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Введён неверный пароль')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(f'Аккаунт {email} заблокирован')
        return super(UserLoginForm, self).clean()

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль ещё раз'}))
    is_subscribed = forms.BooleanField(initial='True', required=False,
                                       widget=forms.CheckboxInput(attrs={'checked' : 'checked'}))

    class Meta:
        model = User
        fields = ['email', 'is_subscribed']
        labels = ''

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = Skill.objects.filter(name__in=top_skills)

    class Meta:
        model = User
        fields = ['city', 'skills', 'is_subscribed', 'remote']
        widgets= {'city' : forms.Select(),
                  'skills' : forms.CheckboxSelectMultiple(),
                  'remote' : forms.CheckboxInput()
                  }

class MyPassChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class MyPassResetForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''

