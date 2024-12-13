from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('how-to-play/', views.how_to_play, name='how_to_play'),
    path('create-game/', views.create_game, name='create_game'),
    path('join-game/', views.join_game, name='join_game'),
    path('game-room/<str:room_code>/', views.game_room, name='game_room'),
    path('game-list/', views.game_list, name='game_list'),
    path('player-scores/<str:room_code>/', views.player_scores, name='player_scores'),
]
