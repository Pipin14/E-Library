
# from django import forms
# from .models import Book

# # class BookUploadForm(forms.ModelForm):
# #     class Meta:
# #         model = Book
# #         fields = ['cover_image', 'title', 'description', 'author', 'genre', 'publication_year', 'page_count']
# #         widgets = {
# #             'cover_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
# #         }


# class BookUploadForm(forms.ModelForm):
#     pdf_file = forms.FileField(required=True, label='File PDF')

#     class Meta:
#         model = Book
#         fields = ['pdf_file', 'title', 'description', 'author', 'publication_year', 'genre']
import logging
from django import forms
from .models import Book

logger = logging.getLogger(__name__)

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'title', 'description', 'author', 'publication_year', 'genre', 'page_count']

    def save(self, commit=True):
        logger.debug("Form disubmit dan data akan disimpan")
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            logger.debug(f"Buku berhasil disimpan dengan ID: {instance.id}")
        return instance
