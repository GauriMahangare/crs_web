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
# Models for content filtering based on cosine similarity
similarity = pickle.load(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/content_filtering/cosine_similarity.pkl", 'rb'))
movie_tag_df = pickle.load(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/content_filtering/movies.pkl", 'rb'))
# Models for content filtering for top trending movies
top_trending_movies_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/data/processed/outputs/top_trending_content.csv", 'r'))
genres_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/data/processed/entity/entity_movie_genres.csv", 'r'))
# Models for collaborative filtering item-item similarity
collab_similarity = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/collab_filtering_item_item_similarity/collab_similarity.pkl", 'rb'))
collab_ratings_pt_indexes = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/collab_filtering_item_item_similarity/collab_ratings_pt_indexes.pkl", 'rb'))
collab_ratings_pt = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/collab_filtering_item_item_similarity/collab_ratings_pt.pkl", 'rb'))
movie_list_full_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/data/processed/movieLense/movies_combined_cleaned_title.csv", 'r'))

# Models for collaborative filtering user-user similarity
collab_u2u_similarity = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/collab_filtering_user_user_similarity/collab_similarity.pkl", 'rb'))
collab_u2u_ratings_pt = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/models/collab_filtering_user_user_similarity/collab_ratings_pt.pkl", 'rb'))
users_list_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/data/processed/movieLense/users.csv", 'r'))
ratings_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/DS/crs_ds/data/processed/movieLense/ratings_short.csv", 'r'))


def remove_special_characters(text):
    # Define a pattern to keep only alphanumeric characters
    pattern = re.compile(r'[^a-zA-Z0-9\s]')

    # Use the pattern to replace non-alphanumeric characters with an empty string
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text

# Search for the value in the list of tuples


def find_index(movie):
    search_value = movie_list_full_df[movie_list_full_df['cleaned_title'].isin([movie])]['imdb_id'].values[0]
    found_tuples = [tup for tup in collab_ratings_pt_indexes if search_value in tup]

    # Display the result
    if found_tuples:
        print(f"Found tuples containing '{search_value}':")
        for found_tuple in found_tuples:
            print(found_tuple)
            print(found_tuple[0])
        return found_tuple[0]
    else:
        print(f"No tuples containing '{search_value}' found.")
        return None


@login_required()
def content_filtering_cosine_similarity(request):
    '''
    View to handle ajax request to recommend movies
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            cleaned_movie = remove_special_characters(data['movieTitle'].lower().strip()).replace(" ", "")
            find_movie = movie_tag_df[movie_tag_df['cleaned_title'].str.contains(cleaned_movie)]
            if find_movie.empty:
                print("Movie not found in DB - " + movie)
                return None
            else:
                movie_index = find_movie.index[0]
                distances = similarity[movie_index]
                movies_recom_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
                if movies_recom_list == None:
                    print("Movie not in database.")
                else:
                    m_list = []
                    for i in movies_recom_list:
                        new_list = {'imdb_id': movie_tag_df.iloc[i[0]].imdb_id,
                                    'title': movie_tag_df.iloc[i[0]].title}
                        m_list.append(new_list)
                    return JsonResponse({'list': m_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


def top_trending_movies(request):
    '''
    View to handle ajax request to return top trending movies
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            genres = request.GET.get('genre')
            top_trending_df = top_trending_movies_df[(
                top_trending_movies_df['titleType'] == 'movie') & (top_trending_movies_df['genres'].str.contains(genres))].head(10)
            top_trending_df = top_trending_df.sort_values('weighted_rating', ascending=False)
            if top_trending_df.empty:
                return JsonResponse({'status': 'No movies found'}, status=200)
            else:
                top_trending = []
                for index, row in top_trending_df.iterrows():
                    new_list = {'imdb_id': row['tconst'],
                                'title': row['primaryTitle'],
                                'weighted_rating': row['weighted_rating'], }
                    top_trending.append(new_list)
                return JsonResponse({'movies': top_trending}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


@login_required()
def collaborative_filtering_i2i_cosine_similarity(request):
    '''
    View to handle ajax request to recommend movies based on movie to movies similarity
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            cleaned_movie = remove_special_characters(data['movieTitle'].lower().strip()).replace(" ", "")
            index = find_index(cleaned_movie)
            if index == None:
                print("Movie not found in DB - " + movie)
                return None
            else:
                # Get the cosine distance of this movie with respect to other movies from similarity matrix computed above
                distances = collab_similarity[index]
                similar_items = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
                movies = []
                for i in similar_items:
                    movies.append(collab_ratings_pt.index[i[0]])
                recom_movie_df = movie_list_full_df[movie_list_full_df['imdb_id'].isin(movies)]
                m_list = []
                for index, row in recom_movie_df.iterrows():
                    new_list = {'imdb_id': row['imdb_id'],
                                'title': row['title']}
                    m_list.append(new_list)
                return JsonResponse({'list': m_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


@login_required()
def collaborative_filtering_u2u_cosine_similarity(request):
    '''
    View to handle ajax request to recommend movies based on user to user similarity
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            index = data['user_id']
            distances = collab_u2u_similarity[index]
            similar_users = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:30]
            users = []
            for u_touple in similar_users:
                # Append users only if Cosine Similarity > 0.3
                if u_touple[1] > 0.3:
                    # print("score - " + str(u_touple[1]))
                    users.append(u_touple[0])
            if users == []:
                print("No users matching with similarity score > 0.3")
                return JsonResponse({'status': 'No users matching with similarity score > 0.3'}, status=200)
            else:
                movies_watched_by_other_similar_users = ratings_df[ratings_df['user_id'].isin(users)]
                rated_movies = ratings_df[ratings_df.user_id == index]["imdb_id"].values
                movies_filtered = movies_watched_by_other_similar_users[movies_watched_by_other_similar_users.imdb_id.apply(
                    lambda imdb_id: imdb_id not in rated_movies)]
                unique_values_list = movies_filtered['imdb_id'].unique().tolist()[:6]
                # Movies rated by this user
                rated_by_user = movie_list_full_df[movie_list_full_df['imdb_id'].isin(rated_movies)].head(10)
                r_list = []
                for index, row in rated_by_user.iterrows():
                    new_list = {'imdb_id': row['imdb_id'],
                                'title': row['title']}
                    r_list.append(new_list)
                print(r_list)
                # Movies recommended to this user
                recomm_movies = movie_list_full_df[movie_list_full_df['imdb_id'].isin(unique_values_list)]
                m_list = []
                for index, row in recomm_movies.iterrows():
                    new_list = {'imdb_id': row['imdb_id'],
                                'title': row['title']}
                    m_list.append(new_list)
                print(m_list)
                return JsonResponse({'recommeded_list': m_list, 'watched_list': r_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


class MovieContentFilteringListView(TemplateView):
    template_name = "movies/movie_content_recomm_form.html"
    context_object_name = "movie_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_list = movie_tag_df['title'].values
        # context["form"] = MovieForm()
        context["movie_list"] = movie_list
        return context


class MovieCollabFilteringi2iCSListView(TemplateView):
    template_name = "movies/movie_collab_i2i_cosine_similarity.html"
    context_object_name = "movie_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_list = movie_tag_df['title'].values
        # context["form"] = MovieForm()
        context["movie_list"] = movie_list
        return context


class MovieCollabFilteringu2uCSListView(TemplateView):
    template_name = "movies/movie_collab_u2u_cosine_similarity.html"
    context_object_name = "user_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = users_list_df['id'].values
        # context["form"] = MovieForm()
        context["user_list"] = user_list
        return context


class MovieCategoriesListView(TemplateView):
    template_name = "movies/movie_top_trending.html"
    context_object_name = "movie_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres_list = genres_df['genres'].values
        # context["form"] = MovieForm()
        context["genres_list"] = genres_list
        return context

# class MovieCreateView(CreateView):
#     model = models.Movie
#     form_class = forms.MovieForm
#     success_url = "/"
