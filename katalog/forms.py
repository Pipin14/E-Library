import logging
from django import forms
from .models import Book

logger = logging.getLogger(__name__)

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'title', 'description', 'author', 'publication_year', 'genre', 'page_count']

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            logger.debug(f"Buku berhasil disimpan dengan ID: {instance.id}")
        
        return instance
