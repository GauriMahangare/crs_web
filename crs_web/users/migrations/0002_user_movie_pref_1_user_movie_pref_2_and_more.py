# Generated by Django 4.2.5 on 2024-01-31 00:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="movie_pref_1",
            field=models.CharField(
                choices=[
                    ("Documentary", "Documentary"),
                    ("Animation", "Animation"),
                    ("Comedy", "Comedy"),
                    ("Short", "Short"),
                    ("Romance", "Romance"),
                    ("News", "News"),
                    ("Drama", "Drama"),
                    ("Fantasy", "Fantasy"),
                    ("Horror", "Horror"),
                    ("Biography", "Biography"),
                    ("Music", "Music"),
                    ("Crime", "Crime"),
                    ("Family", "Family"),
                    ("Adventure", "Adventure"),
                    ("Action", "Action"),
                    ("History", "History"),
                    ("Mystery", "Mystery"),
                    ("Musical", "Musical"),
                    ("War", "War"),
                    ("Sci-Fi", "Sci-Fi"),
                    ("Western", "Western"),
                    ("Thriller", "Thriller"),
                    ("Sport", "Sport"),
                    ("Film-Noir", "Film-Noir"),
                    ("Talk-Show", "Talk-Show"),
                    ("Game-Show", "Game-Show"),
                    ("Adult", "Adult"),
                    ("Reality-TV", "Reality-TV"),
                ],
                default="",
                max_length=60,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="movie_pref_2",
            field=models.CharField(
                choices=[
                    ("Documentary", "Documentary"),
                    ("Animation", "Animation"),
                    ("Comedy", "Comedy"),
                    ("Short", "Short"),
                    ("Romance", "Romance"),
                    ("News", "News"),
                    ("Drama", "Drama"),
                    ("Fantasy", "Fantasy"),
                    ("Horror", "Horror"),
                    ("Biography", "Biography"),
                    ("Music", "Music"),
                    ("Crime", "Crime"),
                    ("Family", "Family"),
                    ("Adventure", "Adventure"),
                    ("Action", "Action"),
                    ("History", "History"),
                    ("Mystery", "Mystery"),
                    ("Musical", "Musical"),
                    ("War", "War"),
                    ("Sci-Fi", "Sci-Fi"),
                    ("Western", "Western"),
                    ("Thriller", "Thriller"),
                    ("Sport", "Sport"),
                    ("Film-Noir", "Film-Noir"),
                    ("Talk-Show", "Talk-Show"),
                    ("Game-Show", "Game-Show"),
                    ("Adult", "Adult"),
                    ("Reality-TV", "Reality-TV"),
                ],
                default="",
                max_length=60,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="movie_pref_3",
            field=models.CharField(
                choices=[
                    ("Documentary", "Documentary"),
                    ("Animation", "Animation"),
                    ("Comedy", "Comedy"),
                    ("Short", "Short"),
                    ("Romance", "Romance"),
                    ("News", "News"),
                    ("Drama", "Drama"),
                    ("Fantasy", "Fantasy"),
                    ("Horror", "Horror"),
                    ("Biography", "Biography"),
                    ("Music", "Music"),
                    ("Crime", "Crime"),
                    ("Family", "Family"),
                    ("Adventure", "Adventure"),
                    ("Action", "Action"),
                    ("History", "History"),
                    ("Mystery", "Mystery"),
                    ("Musical", "Musical"),
                    ("War", "War"),
                    ("Sci-Fi", "Sci-Fi"),
                    ("Western", "Western"),
                    ("Thriller", "Thriller"),
                    ("Sport", "Sport"),
                    ("Film-Noir", "Film-Noir"),
                    ("Talk-Show", "Talk-Show"),
                    ("Game-Show", "Game-Show"),
                    ("Adult", "Adult"),
                    ("Reality-TV", "Reality-TV"),
                ],
                default="",
                max_length=60,
            ),
            preserve_default=False,
        ),
    ]