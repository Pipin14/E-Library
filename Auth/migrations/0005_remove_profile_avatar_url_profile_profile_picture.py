# Generated by Django 5.1.3 on 2024-11-14 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
