from django.urls import path

from . import views


urlpatterns = [
    path('ajax/create-conversation/', views.create_conversation, name='creat-conversation'),
]
