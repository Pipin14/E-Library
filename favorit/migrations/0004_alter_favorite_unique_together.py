# Generated by Django 5.1.3 on 2024-11-15 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorit', '0003_alter_favorite_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=set(),
        ),
    ]
