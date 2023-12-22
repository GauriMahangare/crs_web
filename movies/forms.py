# forms.py
from django import forms
from django_select2 import forms as s2forms
from . import models


class MovieForm(forms.Form):
    movie_choices = ["Topman", "Batmap", "Superman", "He-man",]
    movie = forms.ChoiceField(widget=s2forms.Select2Widget, choices=movie_choices)

# class MovieWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "title__icontains",
#         "cleaned_title"
#     ]

# class MovieForm(forms.ModelForm):
#     class Meta:
#         model = models.Movie
#         fields = "__all__"
#         widgets = {
#             "movie": MovieWidget,
#         }
