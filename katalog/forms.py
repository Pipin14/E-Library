import logging
from django import forms
from .models import Book

logger = logging.getLogger(__name__)

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'cover_image', 'title', 'description', 'author', 'publication_year', 'genre', 'page_count']

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            logger.debug(f"Buku berhasil disimpan dengan ID: {instance.id}")
        
        return instance

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover_image', 'title', 'description', 'author', 'genre', 'publication_year', 'page_count']


class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Cari', widget=forms.TextInput(attrs={'placeholder': 'Cari judul, tahun, deskripsi'}))
