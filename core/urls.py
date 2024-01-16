from django.urls import path
from .views import *
urlpatterns = [
	path('', MainView.as_view(), name='main'),
	path('menu/', MenuView.as_view(), name='menu'),
	path('db/league/', LeagueView.as_view(), name='league_list'),
	path('db/league/<int:league_id>', LeagueDetailView.as_view(), name='league_details'),
	path('db/team', TeamView.as_view(), name='team_list'),
	path('db/team/<int:team_id>', TeamDetailView.as_view(), name='team_details'),
	path('db/match', MatchView.as_view(), name='match_list'),
	path('db/match/info/<int:fixture_id>', MatchDetailView.as_view(), name='match_details'),
	path('db/match/predict/<int:fixture_id>', MatchPredictionView.as_view(), name='match_prediction'),
]
