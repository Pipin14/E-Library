from django.db import models
from django.conf import settings
from django.db import models
from katalog.models import Book
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    page_count = models.IntegerField()
    cover_image = models.ImageField(upload_to='books/covers/')
    pdf_file = models.FileField(upload_to='books/pdf', blank=True, null=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorit_set')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.book.title}"



