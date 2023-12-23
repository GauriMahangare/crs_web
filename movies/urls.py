from django.urls import include, path

from . import views

app_name = "movie"

urlpatterns = [
    # path("create/", views.MovieCreateView.as_view(), name="movie-create"),
    path("content-filtering/", views.MovieContentFilteringListView.as_view(), name="movie-content-list"),
    path("collaborative-filtering/item-item-CS/",
         views.MovieCollabFilteringi2iCSListView.as_view(), name="movie-collab-i2iCS-list"),
    path("collaborative-filtering/user-user-CS/",
         views.MovieCollabFilteringu2uCSListView.as_view(), name="movie-collab-u2uCS-list"),

    path("home/", views.MovieCategoriesListView.as_view(), name="movie-top-trending-list"),

    path('ajax/content-recommend-movies/', views.content_filtering_cosine_similarity, name='content-recommend-movies'),
    path('ajax/collab-recommend-i2i-cosine-similarity/',
         views.collaborative_filtering_i2i_cosine_similarity, name='collab-i2i-CS-recommend-movies'),
    path('ajax/collab-recommend-u2u-cosine-similarity/',
         views.collaborative_filtering_u2u_cosine_similarity, name='collab-u2u-CS-recommend-movies'),
    path('ajax/top-trending-movies', views.top_trending_movies, name='top-trending-movies'),
]
