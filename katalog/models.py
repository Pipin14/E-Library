import logging
from django.db import models

logger = logging.getLogger(__name__)


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

    def save(self, *args, **kwargs):
        logger.debug(f"Saving book: {self.title}")
        if self.pdf_file:
            logger.debug(f"PDF file: {self.pdf_file.name}")
        if self.cover_image:
            logger.debug(f"Cover image: {self.cover_image.name}")
        super().save(*args, **kwargs)
