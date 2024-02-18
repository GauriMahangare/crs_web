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
# from django_select2 import forms as s2forms
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import re

tf.saved_model.LoadOptions(
    allow_partial_checkpoint=False,
    experimental_io_device='/job:localhost',
    experimental_skip_checkpoint=False,
)

logger = logging.getLogger(__name__)
User = get_user_model()
# Models for content filtering based on cosine similarity
similarity = pickle.load(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/content_filtering/cosine_similarity.pkl", 'rb'))
movie_tag_df = pickle.load(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/content_filtering/movies.pkl", 'rb'))
# Models for content filtering for top trending movies
top_trending_movies_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/data/processed/outputs/top_trending_content.csv", 'r'))
genres_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/data/processed/entity/entity_movie_genres.csv", 'r'))
# Models for collaborative filtering item-item similarity
# collab_similarity = pd.read_pickle(
#     open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/collab_filtering_item_item_similarity/collab_similarity.pkl", 'rb'))
# collab_ratings_pt_indexes = pd.read_pickle(
#     open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/collab_filtering_item_item_similarity/collab_ratings_pt_indexes.pkl", 'rb'))
# collab_ratings_pt = pd.read_pickle(
#     open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/collab_filtering_item_item_similarity/collab_ratings_pt.pkl", 'rb'))
movie_list_full_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/data/processed/movieLense/movies_combined_cleaned_title.csv", 'r'))

# # Models for collaborative filtering user-user similarity
# collab_u2u_similarity = pd.read_pickle(
#     open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/collab_filtering_user_user_similarity/collab_similarity.pkl", 'rb'))
# collab_u2u_ratings_pt = pd.read_pickle(
#     open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/collab_filtering_user_user_similarity/collab_ratings_pt.pkl", 'rb'))
users_list_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/data/processed/movieLense/users.csv", 'r'))
ratings_df = pd.read_csv(open(
    "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/data/processed/movieLense/ratings_short.csv", 'r'))

# Models for DNN
path = "/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/DNN_ratings_prediction/cf_dnn_model"
DNN_ratings_model = tf.keras.models.load_model(path)

DNN_ratings_model_df = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/DNN_ratings_prediction/dnn_ratings_pred_df.pkl", 'rb'))
DNN_movie2movie_encoded = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/DNN_ratings_prediction/dnn_movie2movie_encoded.pkl", 'rb'))
DNN_user2user_encoded = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/DNN_ratings_prediction/dnn_user2user_encoded.pkl", 'rb'))
DNN_movie_encoded2movie = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/DNN_ratings_prediction/dnn_movie_encoded2movie.pkl", 'rb'))

# models for matrix factorisation
U_reg = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/matrix_factorisation/user_embedding.pkl", 'rb'))
V_reg = pd.read_pickle(
    open("/Users/gauridhumal/Development Projects/UOL-PROJECTs/CRS/crs_ds/models/matrix_factorisation/item_embedding.pkl", 'rb'))


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
        return found_tuples[0]
    else:
        print(f"No tuples containing '{search_value}' found.")
        return None


def compute_scores(query_embedding, item_embeddings, measure):
    """Computes the scores of the candidates given a query.
    Args:
      query_embedding: a vector of shape [k], representing the query embedding.
      item_embeddings: a matrix of shape [N, k], such that row i is the embedding
        of item i.
      measure: a string specifying the similarity measure to be used. Can be
        either DOT or COSINE.
    Returns:
      scores: a vector of shape [N], such that scores[i] is the score of item i.
    """
    q = query_embedding
    I = item_embeddings
    if measure == "COSINE":
        I = I / np.linalg.norm(I, axis=1, keepdims=True)
        q = q / np.linalg.norm(q)
    scores = q.dot(I.T)
    return scores


def user_recommendations(measure, query_embedding, item_embeddings):
    scores = compute_scores(query_embedding, item_embeddings, measure)
    score_key = measure+"_" + 'score'
    df = pd.DataFrame({
        'score_key': list(scores),
        'movie_id': movie_list_full_df['imdb_id'],
        'titles': movie_list_full_df['title'],
        'genres': movie_list_full_df['genre_tags'],
    })
    return df


def movie_neighbours(title_substring, measure, k, query_embedding, item_embeddings):
    # Select the most matching title
    print(movie_list_full_df.columns)
    title_substring = remove_special_characters(title_substring).lower().replace(" ", "")
    print(title_substring)
    ids = movie_list_full_df[movie_list_full_df['cleaned_title'].str.contains(title_substring)].index.values
    print(ids)
    titles = movie_list_full_df.iloc[ids]['title'].values
    if len(titles) == 0:
        # raise ValueError("Found no movies with title %s" % title_substring)
        other_matching_titles = "Found no movies with title %s" % title_substring
        df = pd.DataFrame()
        return df, other_matching_titles
    else:
        print("Nearest neighbors of : %s." % titles[0])
        print("[Found more than one matching movie. Other candidates: {}]".format(
            ", ".join(titles[1:])))
        other_matching_titles = ", ".join(titles[0:])
        movie_id = ids[0]

        query_embedding = query_embedding[movie_id]
    # Calculating dot matrix this the most matched movie with other movie embeddings to find the other matching movies
        scores = compute_scores(query_embedding, item_embeddings, measure)

        score_key = measure + "_" + "score"
        # df['score_key'] = list(scores),
        # df['movie_id'] = movie_list_full_df['imdb_id'],
        # df['titles'] = movie_list_full_df['title'],
        # df['genres'] = movie_list_full_df['genre_tags'],
        df = pd.DataFrame({
            score_key: list(scores),
            'movie_id': movie_list_full_df['imdb_id'],
            'titles': movie_list_full_df['title'],
            'genres': movie_list_full_df['genre_tags'],
        })
        print(df)
        print(type(df))
        print(other_matching_titles)
        return df, other_matching_titles


@login_required()
def collaborative_filtering_mf_user(request):
    '''
    View to handle ajax request to recommend movies based on matrix factorisation algorithm
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            print("inside MF User")
            data = json.load(request)
            user_id = data['user_id']
            measure = data['measure']
            exclude_rated = data['exclude_rated']
            print(user_id)
            print(measure)
            print(exclude_rated)
            k = 5  # Number of movies to be recommended
            # Create the query embeddings
            query_embedding = U_reg.numpy()[user_id]
            item_embeddings = V_reg.numpy()

            df = user_recommendations(measure, query_embedding, item_embeddings)
            print(df)
            score_key = measure + "_" + "score"
            rated_movies = ratings_df[ratings_df.user_id == user_id]["movie_id"].values
            rated_movies_df = ratings_df[ratings_df.user_id == user_id]["movie_id"]
            top_movies_user = rated_movies_df.sort_values(ascending=False).head(5)
            movie_df_rows = movie_list_full_df[movie_list_full_df["ml_id"].isin(top_movies_user)]

            if exclude_rated == "Yes":
                # remove movies that are already rated
                df = df[df.movie_id.apply(lambda movie_id: movie_id not in rated_movies)]
            recom_movie_df = df.sort_values(["score_key"], ascending=False).head(k)
            m_list = []
            for index, row in recom_movie_df.iterrows():
                new_list = {'imdb_id': row['movie_id'],
                            'title': row['titles'],
                            'genres': row['genres']}
                m_list.append(new_list)
            r_list = []
            print(type(rated_movies))
            print(rated_movies)
            for index, row in movie_df_rows.iterrows():
                new_list = {'imdb_id': row['imdb_id'],
                            'title': row['title'],
                            'genres': row['genre_tags']}
                r_list.append(new_list)
            return JsonResponse({'recommeded_list': m_list, 'watched_list': r_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


@login_required()
def collaborative_filtering_mf_nearest_neighbour(request):
    '''
    View to handle ajax request to recommend movies based on matrix factorisation algorithm
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            print("In nearest neighbours")
            print(data)
            title_substring = data['title_substring']
            measure = data['measure']  # DOT or Cosine Similarity
            print(title_substring)
            print(measure)
            score_key = measure+"_" + 'score'
            k = 5  # Number of movies to be recommended
            # Create the query embeddings
            query_embedding = V_reg.numpy()
            item_embeddings = V_reg.numpy()
            df, other_matching_titles = movie_neighbours(title_substring, measure, k, query_embedding, item_embeddings)
            print(df)
            m_list = [{'other_matching_titles': other_matching_titles}]
            if df.empty:
                print("No movies found")
                # return JsonResponse("No movies found", status=200)
            else:
                recom_movie_df = df.sort_values([score_key], ascending=False).head(k)

                # df = user_recommendations(measure, query_embedding, item_embeddings)
                # print(df)
                # recom_movie_df = df.sort_values(["score_key"], ascending=False).head(k)

                for index, row in recom_movie_df.iterrows():
                    new_list = {'imdb_id': row['movie_id'],
                                'title': row['titles'],
                                'genres': row['genres'],
                                }
                    m_list.append(new_list)
            return JsonResponse({'recommeded_list': m_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


@login_required()
def content_filtering_search(request):
    '''
    View to handle ajax request to recommend movies
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            search_string = remove_special_characters(data['movieTitle'].lower().strip()).replace(" ", "")
            searched_movies = movie_tag_df[movie_tag_df['tags'].str.contains(search_string)]
            if searched_movies.empty:
                print("String not found in tag - " + search_string)
                searched_movies = movie_tag_df[movie_tag_df['cleaned_title'].str.contains(search_string)]
                if searched_movies.empty:
                    search_list = []
                    print("String not found in title - " + search_string)
                    return JsonResponse({'search_list': search_list}, status=200)
                else:
                    search_list = []
                    for index, row in searched_movies.iterrows():
                        print(f"Index: {index}, Values: {row['ml_id']}, {row['title']}, {row['imdb_id']}")
                        new_list = {'index': index,
                                    'imdb_id': row['imdb_id'],
                                    'title': row['title'],
                                    'tags': row['tags']}
                        search_list.append(new_list)
                    return JsonResponse({'search_list': search_list}, status=200)
            else:
                search_list = []
                for index, row in searched_movies.iterrows():
                    print(f"Index: {index}, Values: {row['ml_id']}, {row['title']}, {row['imdb_id']}")
                    new_list = {'index': index,
                                'imdb_id': row['imdb_id'],
                                'title': row['title'],
                                'tags': row['tags']}
                    search_list.append(new_list)
                return JsonResponse({'search_list': search_list}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


@login_required()
def content_filtering_cosine_similarity(request, index):
    '''
    View to handle ajax request to recommend movies
    '''
    print("in content_filtering_cosine_similarity")
    print(request.headers)
    # is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    # if is_ajax:
    if request.method == 'GET':
        movie_index = index
        print(movie_index)
        distances = similarity[movie_index]
        movies_recom_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
        m_list = []
        if movies_recom_list == None:
            print("No movies to recommend.")
        else:
            for i in movies_recom_list:
                new_list = {'imdb_id': movie_tag_df.iloc[i[0]].imdb_id,
                            'title': movie_tag_df.iloc[i[0]].title}
                m_list.append(new_list)
        return JsonResponse({'recommend_list': m_list}, status=200)
    return JsonResponse({'status': 'Invalid request'}, status=400)
    # else:
    #     return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


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


# @login_required()
# def collaborative_filtering_i2i_cosine_similarity(request):
#     '''
#     View to handle ajax request to recommend movies based on movie to movies similarity
#     '''
#     is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#     if is_ajax:
#         if request.method == 'POST':
#             data = json.load(request)
#             cleaned_movie = remove_special_characters(data['movieTitle'].lower().strip()).replace(" ", "")
#             index = find_index(cleaned_movie)
#             print(index)
#             if index == None:
#                 print("Movie not found in DB - " + cleaned_movie)
#                 return None
#             else:
#                 # Get the cosine distance of this movie with respect to other movies from similarity matrix computed above
#                 distances = collab_similarity[index[0]]
#                 similar_items = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#                 movies = []
#                 for i in similar_items:
#                     movies.append(collab_ratings_pt.index[i[0]])
#                 recom_movie_df = movie_list_full_df[movie_list_full_df['imdb_id'].isin(movies)]
#                 m_list = []
#                 for index, row in recom_movie_df.iterrows():
#                     new_list = {'imdb_id': row['imdb_id'],
#                                 'title': row['title']}
#                     m_list.append(new_list)
#                 return JsonResponse({'list': m_list}, status=200)
#         return JsonResponse({'status': 'Invalid request'}, status=400)
#     else:
#         return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


# @login_required()
# def collaborative_filtering_u2u_cosine_similarity(request):
#     '''
#     View to handle ajax request to recommend movies based on user to user similarity
#     '''
#     is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#     if is_ajax:
#         if request.method == 'POST':
#             data = json.load(request)
#             index = data['user_id']
#             distances = collab_u2u_similarity[index]
#             similar_users = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:30]
#             users = []
#             for u_touple in similar_users:
#                 # Append users only if Cosine Similarity > 0.3
#                 if u_touple[1] > 0.3:
#                     # print("score - " + str(u_touple[1]))
#                     users.append(u_touple[0])
#             if users == []:
#                 print("No users matching with similarity score > 0.3")
#                 return JsonResponse({'status': 'No users matching with similarity score > 0.3'}, status=200)
#             else:
#                 movies_watched_by_other_similar_users = ratings_df[ratings_df['user_id'].isin(users)]
#                 rated_movies = ratings_df[ratings_df.user_id == index]["imdb_id"].values
#                 movies_filtered = movies_watched_by_other_similar_users[movies_watched_by_other_similar_users.imdb_id.apply(
#                     lambda imdb_id: imdb_id not in rated_movies)]
#                 unique_values_list = movies_filtered['imdb_id'].unique().tolist()[:6]
#                 # Movies rated by this user
#                 rated_by_user = movie_list_full_df[movie_list_full_df['imdb_id'].isin(rated_movies)].head(10)
#                 r_list = []
#                 for index, row in rated_by_user.iterrows():
#                     new_list = {'imdb_id': row['imdb_id'],
#                                 'title': row['title']}
#                     r_list.append(new_list)
#                 print(r_list)
#                 # Movies recommended to this user
#                 recomm_movies = movie_list_full_df[movie_list_full_df['imdb_id'].isin(unique_values_list)]
#                 m_list = []
#                 for index, row in recomm_movies.iterrows():
#                     new_list = {'imdb_id': row['imdb_id'],
#                                 'title': row['title']}
#                     m_list.append(new_list)
#                 print(m_list)
#                 return JsonResponse({'recommeded_list': m_list, 'watched_list': r_list}, status=200)
#         return JsonResponse({'status': 'Invalid request'}, status=400)
#     else:
#         return JsonResponse({'status': 'Invalid AJAX request'}, status=400)


@login_required()
def dnn_ratings_predictions(request):
    '''
    View to handle ajax request to recommend movies based on DNN model for ratings predictions
    '''
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            user_id = data['user_id']
            movies_watched_by_user = DNN_ratings_model_df[DNN_ratings_model_df.user_id == user_id]
            movies_not_watched = movie_list_full_df[
                ~movie_list_full_df["ml_id"].isin(movies_watched_by_user.movie_id.values)]["ml_id"]
            # extract movies from not watch list that other users have rated
            movies_not_watched = list(set(movies_not_watched).intersection(set(DNN_movie2movie_encoded.keys())))
            # extract the index of these
            movies_not_watched = [[DNN_movie2movie_encoded.get(x)] for x in movies_not_watched]
            # get user index
            user_encoder = DNN_user2user_encoded.get(user_id)
            user_input = np.array([[user_encoder]] * len(movies_not_watched))
            movies_input = np.array(movies_not_watched)
            # predict user ratings on unseen movies
            user_ratings = DNN_ratings_model.predict([user_input, movies_input]).flatten()
            print(user_ratings)
            # Select top 10 movies with highest ratings
            top_ratings_indices = user_ratings.argsort()[-10:][::-1]
            # Get the original movie ids for recommended movies
            recommended_movie_ids = [DNN_movie_encoded2movie.get(
                movies_not_watched[x][0]) for x in top_ratings_indices]
            top_movies_user = (
                movies_watched_by_user.sort_values(by="rating", ascending=False).head(5).movie_id.values)
            movie_df_rows = movie_list_full_df[movie_list_full_df["ml_id"].isin(top_movies_user)]
            r_list = []
            for index, row in movie_df_rows.iterrows():
                new_list = {'imdb_id': row['imdb_id'],
                            'title': row['title']}
                r_list.append(new_list)
            print(r_list)
            # Movies recommended to this user
            recomm_movies = movie_list_full_df[movie_list_full_df["ml_id"].isin(recommended_movie_ids)]
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


class MovieDNNRatingsPredListView(TemplateView):
    template_name = "movies/movie_collab_DNN_ratings.html"
    context_object_name = "user_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = users_list_df['id'].values
        # context["form"] = MovieForm()
        context["user_list"] = user_list
        return context


class MovieMFUser(TemplateView):
    template_name = "movies/movie_collab_MF_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = users_list_df['id'].values
        # context["form"] = MovieForm()
        context["user_list"] = user_list
        context["measure_list"] = ["COSINE", "DOT"]
        context["exclude_rated"] = ["Yes", "No"]
        return context


class MovieMFNearestNeighbour(TemplateView):
    template_name = "movies/movie_collab_MF_nearest_neighbour.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["measure_list"] = ["COSINE", "DOT"]
        context["exclude_rated"] = ["Yes", "No"]
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
