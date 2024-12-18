# Generated by Django 5.1.3 on 2024-11-16 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorit', '0007_alter_favorite_book'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_books', to='favorit.book'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorit_user_favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='created_at',
        ),
    ]
