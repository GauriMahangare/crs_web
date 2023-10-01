from django.urls import path

from . import views


urlpatterns = [

    # path("<str:room_name>/", views.room, name="room"),
    # #
    # path('api/creat-room/<str:uuid>', views.create_room, name='creat-room')
    path('ajax/create-conversation/', views.create_conversation, name='creat-conversation')
]
