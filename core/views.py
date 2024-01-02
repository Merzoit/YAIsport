from django.shortcuts import render
from django.views.generic import TemplateView, View
# Create your views here.
from .data import *
api_client = YAPIClient()
#api_client.get_league('Germany', 2023)
#api_client.get_all_team()
#api_client.get_all_standings()
#api_client.get_all_player()
#api_client.get_all_coach()
#api_client.get_coach(80)
#api_client.get_team_statistic(2023, 85, 61)
#api_client.get_all_team_statistic()
#api_client.get_fixture(61, '2024-01-01', '2024-30-01')
#api_client.get_all_fixture('2024-01-01', '2024-30-01')
#api_client.get_all('2024-01-01', '2024-30-01')
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
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league_id = kwargs.get('league_id')
		context['league'] = League.objects.get(id=league_id)
		context['league_table'] = LeagueTable.objects.filter(league = league_id)
		return context