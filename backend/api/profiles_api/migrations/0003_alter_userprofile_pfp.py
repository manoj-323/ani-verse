# Generated by Django 5.1.1 on 2025-01-12 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0002_userprofile_pfp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='pfp',
            field=models.ImageField(blank=True, upload_to='profile_pictures/'),
        ),
    ]
