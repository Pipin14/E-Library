from django.contrib import admin
from django.urls import path, include
from katalog.views import katalog
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import book_list, upload_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', katalog, name='katalog'),
    path('katalog', katalog, name='katalog'),
    path('katalog/', views.katalog_view, name='katalog'),
    path('', book_list, name='book_list'),
    path('upload/', upload_book, name='upload_book'),
    path('favorit/', include('favorit.urls')),
    path('toggle-favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

