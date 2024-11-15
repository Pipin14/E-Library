from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, EditProfileForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
import logging


logger = logging.getLogger(__name__)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('katalog')
            else:
                messages.error(request, "Email atau password salah.")
                logger.warning(f"Failed login attempt for email: {email}")
        else:
            messages.error(request, "Invalid form data.")
            logger.warning(f"Invalid login form data: {form.errors}")
    else:
        form = LoginForm()
    return render(request, 'Auth/login.html', {'form': form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            messages.success(request, "Registrasi berhasil!")
            logger.info(
                "User successfully registered and redirected to katalog.")
            return redirect('katalog')
        else:
            messages.error(
                request, "Terdapat kesalahan pada registrasi. Silakan coba lagi.")
            logger.error("Form validation failed during registration.")
    else:
        form = RegisterForm()

    return render(request, 'Auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'Auth/profile.html')


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        account_form = EditProfileForm(
            request.POST, request.FILES, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=profile)

        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            messages.success(request, "Profil berhasil diperbarui!")
            return redirect('profile')
    else:
        account_form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'Auth/edit_profile.html', {
        'account_form': account_form,
        'profile_form': profile_form
    })


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        # print("Form data:", request.POST)
        # logger.debug("Form data: %s", request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Anda telah berhasil diubah.')
            return redirect('profile')
        else:
            # print("Form errors:", form.errors)
            # logger.error("Form errors: %s", form.errors)

            messages.error(
                request, 'Ada kesalahan pada formulir perubahan password.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'Auth/change_password.html', {'form': form})
