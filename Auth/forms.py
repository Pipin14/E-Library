from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from .models import UserAccount, Profile


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Menggunakan email untuk autentikasi, karena USERNAME_FIELD adalah email
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Email atau Password salah.")
        return cleaned_data


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Konfirmasi Password")

    class Meta:
        model = UserAccount
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserAccount.objects.filter(email=email).exists():
            raise ValidationError(
                "Email sudah digunakan. Silakan pilih email lain.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError(
                "Password dan konfirmasi password tidak sesuai.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Password Baru", required=False)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Konfirmasi Password Baru", required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserAccount
        fields = ['first_name', 'email', 'profile_picture']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise ValidationError(
                "Password dan konfirmasi password tidak sesuai.")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')

        if password1:
            user.set_password(password1)

        if commit:
            user.save()
        return user

# forms.py


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Pastikan profile_picture termasuk di dalam fields
        fields = ['profile_picture']
