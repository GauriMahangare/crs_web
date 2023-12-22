from django.urls import include, path

from . import views

app_name = "movie"

urlpatterns = [
    # path("create/", views.MovieCreateView.as_view(), name="movie-create"),
    path("list/", views.MovieListView.as_view(), name="movie-list"),
    path('ajax/recommend-movies/', views.recommend_based_on_title, name='recommend-movies'),
]
