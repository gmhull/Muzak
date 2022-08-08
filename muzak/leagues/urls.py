from django.urls import path, include, re_path
from . import views
from .views import LeagueListView, LeagueDetailView, LeagueStandingsListView, RoundResultsListView
from .models import League

urlpatterns = [
    # path('', views.league_home, name='league_home'),
    path('', LeagueListView.as_view(), name='league_home'),
    path('<slug:slug>/', include([
        path('', LeagueDetailView.as_view(), name='league_detail'),
        path('standings/', LeagueStandingsListView.as_view(), name='league_standings'),
        path('round_<int:pk>/', include([
            path('', views.league_round, name='league_round'),
            path('voting/', views.round_voting, name='round_voting'),
            path('results/', RoundResultsListView.as_view(), name='round_results'),
            path('submit/', views.song_submission, name='song_submission'),
        ]))
    ]))
]
