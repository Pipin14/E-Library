# Generated by Django 5.1.3 on 2024-11-15 08:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorit', '0002_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'book')},
        ),
    ]
