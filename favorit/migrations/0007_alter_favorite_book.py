# Generated by Django 5.1.3 on 2024-11-16 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorit', '0006_favorite_created_at_alter_favorite_user_and_more'),
        ('katalog', '0007_remove_favorite_created_at_alter_book_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_books', to='katalog.book'),
        ),
    ]