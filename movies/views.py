import json
import logging
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
    TemplateView,
)
from django.http.request import HttpRequest
from django.http import HttpResponseBadRequest, JsonResponse

from . import forms, models
from django import forms
from django_select2 import forms as s2forms
import pickle
import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import re

logger = logging.getLogger(__name__)
User = get_user_model()

similarity = pickle.load(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/cosine_similarity.pkl", 'rb'))
movie_list_df = pickle.load(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/movies.pkl", 'rb'))


def remove_special_characters(text):
    # Define a pattern to keep only alphanumeric characters
    pattern = re.compile(r'[^a-zA-Z0-9\s]')

    # Use the pattern to replace non-alphanumeric characters with an empty string
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text


@login_required()
def recommend_based_on_title(request):
    '''
    View to handle ajax request to recommend movies
    '''
    print("recommend_based_on_title")
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            print(type(data))
            print(data)
            print(data['movieTitle'])
            cleaned_movie = remove_special_characters(data['movieTitle'].lower().strip()).replace(" ", "")
            find_movie = movie_list_df[movie_list_df['cleaned_title'].str.contains(cleaned_movie)]
            print(cleaned_movie)
            if find_movie.empty:
                print("Movie not found in DB - " + movie)
                return None
            else:
                movie_index = find_movie.index[0]
                print(movie_index)

                distances = similarity[movie_index]
                print(distances)
                print(enumerate(distances))
                print(list(enumerate(distances)))
                movies_recom_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
                print(movies_recom_list)
                if movies_recom_list == None:
                    print("Movie not in database.Here are top trending movies...")
                else:
                    m_list = []
                    for i in movies_recom_list:
                        print(movie_list_df.iloc[i[0]].title + "-" + movie_list_df.iloc[i[0]].imdb_id)
                        new_list = {'imdb_id': movie_list_df.iloc[i[0]].imdb_id,
                                    'title': movie_list_df.iloc[i[0]].title}
                        m_list.append(new_list)
                    print(m_list)
                    return JsonResponse({'list': m_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


class MovieForm(forms.Form):
    movie_choices = ["Topman", "Batmap", "Superman", "He-man",]
    movie = forms.ChoiceField(widget=s2forms.Select2Widget, choices=movie_choices)


class MovieListView(TemplateView):
    template_name = "movies/movie_form.html"
    context_object_name = "movie_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_list = pickle.load(
            open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/movies.pkl", 'rb'))
        movie_list = movie_list['title'].values
        # context["form"] = MovieForm()
        context["movie_list"] = movie_list
        return context


# class MovieCreateView(CreateView):
#     model = models.Movie
#     form_class = forms.MovieForm
#     success_url = "/"
