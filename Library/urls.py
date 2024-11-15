from django.contrib import admin
from django.urls import path, include
from katalog import views as katalog_views
from Auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', katalog_views.katalog_view, name='katalog'),
    path('katalog/', include('katalog.urls')),
    path('favorit/', include('favorit.urls')),
    path('auth/', include('Auth.urls')),
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
