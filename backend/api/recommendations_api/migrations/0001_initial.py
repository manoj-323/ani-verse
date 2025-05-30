# Generated by Django 5.1.1 on 2025-01-06 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRecommendationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arm', models.PositiveSmallIntegerField()),
                ('ratings', models.JSONField(default=list)),
                ('t', models.PositiveIntegerField(default=1)),
                ('recommended_shows', models.ManyToManyField(related_name='recommended_shows', to='core.anime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
