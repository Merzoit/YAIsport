from django.shortcuts import render
from django.views.generic import TemplateView, View
from datetime import datetime, date
import pytz
from django.db.models import Q
from django import template
from football.settings import BASE_DIR

#get_league_task.delay()

# Create your views here.
from core.data import *
from core.algorythm import *

algorythm = YAIalgorythm()
api_client = YAPIClient()
#api_client.get_league('England', 2023)
#api_client.get_all_team()
#api_client.get_team(79)
#api_client.get_all_standings()
#api_client.get_standings(79)
#api_client.get_all_player()
#api_client.get_all_coach()
#api_client.get_coach()
#api_client.get_team_statistic(2023, 85, 61)
#api_client.get_all_team_statistic()
#api_client.get_fixture(61, '2024-01-01', '2024-30-01')
#api_client.get_all_fixture()
#api_client.get_all('2024-01-01', '2024-30-01')
#api_client.get_all_fixture_statistic()
#api_client.get_fixture_prediction('1035374')
class MainView(TemplateView):
	"""
	Основная страница
	"""
	template_name = 'main.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
		
		
class MenuView(TemplateView):
	"""
	Основная страница
	"""
	template_name = 'menu.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
		
		
class LeagueView(TemplateView):
	"""
	Список лиг
	"""
	template_name = 'league_list.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['leagues'] = League.objects.all()
		return context
		

class LeagueDetailView(TemplateView):
	"""
	Детали лиги
	"""
	template_name = 'league_details.html'
	today = date.today()
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league_id = kwargs.get('league_id')
		context['league'] = League.objects.get(id=league_id)
		context['league_table'] = LeagueTable.objects.filter(league=league_id).order_by('position')
		context['league_fixture'] = Fixture.objects.filter(league=league_id, date__gte=self.today)
		return context
		
		
class TeamView(TemplateView):
	"""
	Детали команды
	"""
	template_name = 'team_list.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['teams'] = Team.objects.all()
		return context
		
    
class TeamDetailView(TemplateView):
	"""
	Детали команды
	"""
	template_name = 'team_details.html'
	today = date.today()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		team_id = kwargs.get('team_id')
		current_team = Team.objects.get(id=team_id)
		context['team'] = Team.objects.get(id=team_id)
		context['players'] = Player.objects.filter(team=current_team)
		context['player_statistic'] = PlayerStatistic.objects.filter(player__team=current_team)
		context['player_data'] = sorted(zip(context['players'], context['player_statistic']), key=lambda x: (x[1].rating), reverse=True)
		context['venue'] = Venue.objects.get(team=current_team)
		context['coach'] = Coach.objects.get(team=current_team)
		context['matches'] = Fixture.objects.filter(Q(team_home=current_team) | Q(team_away=current_team), date__gte=self.today)
		context['table'] = LeagueTable.objects.get(team=current_team)
		context['stat'] = algorythm.team_statistic(team_id=team_id)
		context['top_players'] = {
			'key_player': sorted(context['player_statistic'], key=lambda x: (x.rating), reverse=True)[0],
			'goal_player': sorted(context['player_statistic'], key=lambda x: (x.goals_total), reverse=True)[0],
			'minute_player': sorted(context['player_statistic'], key=lambda x: (x.minutes), reverse=True)[0],
			'passes_player': sorted(context['player_statistic'], key=lambda x: (x.passes_accuracy), reverse=True)[0],
		}
		return context


class MatchView(TemplateView):
	"""
	Список матчей
	"""
	template_name = 'match_list.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fixtures_finished'] = Fixture.objects.filter(status='Match Finished')[:10]
		context['fixtures_waited'] = Fixture.objects.exclude(status='Match Finished')[:10]
		return context


class MatchDetailView(TemplateView):
	"""
	Список матчей
	"""
	template_name = 'match_details.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		fixture_id = kwargs.get('fixture_id')
		context['fixture'] = Fixture.objects.get(id=fixture_id)
		context['fixture_statistic'] = FixtureStatistic.objects.get(fixture=fixture_id)
		return context

class MatchPredictionView(TemplateView):
	"""
	Список матчей
	"""
	template_name = 'match_prediction.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		fixture_id = kwargs.get('fixture_id')
		context['fixture_prediction'] = FixturePrediction.objects.get(fixture=fixture_id)
		return context