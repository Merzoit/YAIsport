from django.urls import path
from .views import *
urlpatterns = [
	path('', MainView.as_view(), name='main'),
	path('menu/', MenuView.as_view(), name='menu'),
	path('db/league/', LeagueView.as_view(), name='league_list'),
	path('db/league/<int:league_id>', LeagueDetailView.as_view(), name='league_details')
]
