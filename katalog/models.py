
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=200)  # Penulis
    genre = models.CharField(max_length=100)  # Genre
    publication_year = models.IntegerField()  # Tahun Terbit
    page_count = models.IntegerField()  # Jumlah Halaman
    cover_image = models.ImageField(upload_to='books/covers/')  # Thumbnail
    is_favorite = models.BooleanField(default=False)  # Untuk tanda buku favorit

    def __str__(self):
        return self.title
