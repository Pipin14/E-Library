# Generated by Django 5.1.3 on 2024-11-17 04:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0012_book_favorited_by_book_is_favorite_useraccount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='favorited_by',
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='katalog_books', to='katalog.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='katalog_user_favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserAccount',
        ),
    ]
