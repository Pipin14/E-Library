
from django import forms
from .models import Book

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover_image', 'title', 'description', 'author', 'genre', 'publication_year', 'page_count']
        widgets = {
            'cover_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # Menambahkan file upload untuk gambar
        }
