from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.favorite_books, name='favorit'),
    path('toggle_favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

