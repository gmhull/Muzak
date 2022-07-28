from django.urls import path, include, re_path
from . import views
from .views import LeagueListView, LeagueDetailView, RoundListView
from .models import League

urlpatterns = [
    # path('', views.league_home, name='league_home'),
    path('', LeagueListView.as_view(), name='league_home'),
    path('<slug:slug>/', include([
        path('', LeagueDetailView.as_view(), name='league_detail'),
        # path('', RoundListView.as_view(), name='league_detail'),
        path('standings/', views.league_standings, name='league_standings'),
        path('round_<int:id>/', include([
            path('', views.league_round, name='league_round'),
            path('voting/', views.round_voting, name='round_voting'),
            path('results/', views.round_results, name='round_results'),
        ]))
    ]))

]
