from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import change_password_view
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('login/register/', views.register_view, name='register'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/',
         views.change_password_view, name='change_password'),
    path('change-password/', change_password_view, name='change_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
