from django.urls import path

from main.views import GetPlayersCountPerRounds, GeTopPlayers, DoScroll

urlpatterns = [
    path('stats/players-count/', GetPlayersCountPerRounds.as_view()),
    path('stats/top-players/', GeTopPlayers.as_view()),
    path('scroll/', DoScroll.as_view()),
]
