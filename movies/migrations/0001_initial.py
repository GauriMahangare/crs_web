# Generated by Django 4.2.5 on 2024-01-31 00:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ml_id", models.IntegerField(blank=True, default=0, verbose_name="Movie Lense ID")),
                ("title", models.CharField(blank=True, max_length=200, verbose_name="Movie Title")),
                ("imdb_id", models.IntegerField(blank=True, default=0, verbose_name="IMDB ID")),
                ("tags", models.TextField()),
                ("cleaned_title", models.CharField(blank=True, max_length=200, verbose_name="Cleaned Movie Title")),
            ],
        ),
    ]
