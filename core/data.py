from core.models import *
from football.settings import API_KEY
import requests
import json
import time
import os
from football.settings import BASE_DIR
from datetime import datetime
from core.utils import Logger
from dateutil import parser

#ЗАПИСЬ ДАННЫХ ЧЕРЕЗ API
class YAPIClient(Logger):
	"""
	Класс с методами для получения данных из API
	"""
	def _make_api_request(self, url):
		headers = {'x-apisports-key': API_KEY}
		response = requests.get(url, headers=headers)
		response.raise_for_status()
		data = response.json()
		return data
			
	def get_league(self, country='France', season=2023):
		"""
		Получить лиги по параметрам:
		1)Страна
		2)Сезон
		"""
		url = f'https://v3.football.api-sports.io/leagues?country={country}&season={season}'
		try:
			#Запрос к АПИ с выбранными параметрами
			data = self._make_api_request(url)
			
			#Обработка ошибок	
			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return
			#Запись или обновление всех имеющихся в RESPONSE данных.
			for league in data['response']:
				#Получение объектов
				country_object = Country.objects.get(name=country)
				season_object = Season.objects.get(year=season)
				
				#Создание объекта лиги
				obj, created = League.objects.update_or_create(
					id = int(league['league']['id']),
					country=country_object,
					season=season_object,
					defaults = {
						'name': league['league']['name'],
						'logo_url': league['league']['logo'],
					}
				)
				self.log_entry(f'SUCCESS: League {league["league"]["id"]} added or updated.')
				
		except Exception as e:
			#Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')
		
	def get_standings(self, league, season=2023):
		"""
		Получить таблицу лиги
		"""
		url = f'https://v3.football.api-sports.io/standings?league={league}&season={season}'
		try:
			#Запрос к АПИ с выбранными параметрами
			data = self._make_api_request(url)
	
			#Обработка ошибок
			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return

			league_object = League.objects.get(id=league)
			data = data['response'][0]['league']['standings'][0]

			#Запись или обновление данных из API
			for team in data:
				obj_table, created = LeagueTable.objects.update_or_create(
					league = league_object,
					team = Team.objects.get(id=team['team']['id']),
					defaults = {
						#Общая статистика
						'position': team['rank'],
						'points': team['points'],
						'form': team['form'],
						'played': team['all']['played'],
						'win': team['all']['win'],
						'draw': team['all']['draw'],
						'lose': team['all']['lose'],
						'goal_for': team['all']['goals']['for'],
						'goal_against': team['all']['goals']['against'],
						#Домашняя статистика
						'played_home': team['home']['played'],
						'win_home': team['home']['win'],
						'draw_home': team['home']['draw'],
						'lose_home': team['home']['lose'],
						'goal_for_home': team['home']['goals']['for'],
						'goal_against_home': team['home']['goals']['against'],	
						#Гостевая статистика
						'played_away': team['away']['played'],
						'win_away': team['away']['win'],
						'draw_away': team['away']['draw'],
						'lose_away': team['away']['lose'],
						'goal_for_away': team['away']['goals']['for'],
						'goal_against_away': team['away']['goals']['against'],
					}
				)
				self.log_entry(f'SUCCESS: Standings for team {team["team"]["id"]} in league {league} added or updated.')	
		except Exception as e:
			self.log_entry(f'DEEP-ERROR: {e}')
			
	def get_team(self, league=0, season=2023):
		"""
		Получить команды по параметрам:
		1)Лига
		2)Сезон
		"""
		#Запрос к АПИ с выбранными параметрами
		url = f'https://v3.football.api-sports.io/teams?league={league}&season={season}'
		#Проверка на статус ответа	
		try:
			data = self._make_api_request(url)
			
			#Обработка ошибок	
			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return
			
			data = data['response']
			#Цикл команд из запроса
			for team in data:
				#Получение объектов из параметров
				league_object = League.objects.get(id=league)
				country_object = Country.objects.get(name=league_object.country)
				season_object = Season.objects.get(year=season)
				#Проверка на существование команды в других лигах
				try:
					teams = Team.objects.get(id=team['team']['id'])
					#Если существует, добавляем лигу команде
					teams.league.add(league_object)
					self.log_entry(f'SUCCESS: League {league_object.id} added to team {team["team"]["id"]}.')
					continue
				except Team.DoesNotExist:
					#Если не существует, продолжаем работу скрипта
					pass
				#Проверка на существование стадиона
				try:
					venue_object = Venue.objects.get(id=team['venue']['id'])
				except Venue.DoesNotExist:
					#Если не существует, создаём объект
					obj, created = Venue.objects.update_or_create(
						id = int(team['venue']['id']),
						defaults = {
							'name': team['venue']['name'],
							'address': team['venue']['address'],
							'city': team['venue']['city'],
							'surface': team['venue']['surface'],
							'capacity': team['venue']['capacity'],
							'image': team['venue']['image'],
						}
					)
					self.log_entry(f'SUCCESS: Venue {team["venue"]["id"]} added to team {team["team"]["id"]}.')
					venue_object = Venue.objects.get(id=team['venue']['id'])
				#Создание объекта лиги
				obj, created = Team.objects.update_or_create(
					id = int(team['team']['id']),
					country=country_object,
					season=season_object,
					venue=venue_object,
					defaults = {
						'name': team['team']['name'],
						'code': team['team']['code'],
						'logo_url': team['team']['logo'],
					}
				)
				self.log_entry(f'SUCCESS: Team {team["team"]["id"]} added or updated.')
				obj.league.add(league_object)
		except Exception as e:
			#Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')
	
	def get_coach(self, team):
		"""
		Метод для получения и записи данных о тренере.
		"""
		
		url = f'https://v3.football.api-sports.io/coachs?team={team}'
		try:
			data = self._make_api_request(url)
			
			#Обработка ошибок	
			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return
			
			coach = data['response'][-1]
			team_object = Team.objects.get(id=team)
				
			obj, created = Coach.objects.update_or_create(
				id=coach['id'],
				team=team_object,
				defaults = {
					'name': coach['name'],
					'first_name': coach['firstname'],
					'last_name': coach['lastname'],
					'age': coach['age'],
					'birthday': coach['birth']['date'],
					'nationality': coach['nationality'],
					'height': coach['height'],
					'weight': coach['weight'],
					'photo': coach['photo'],
				}
			)
			self.log_entry(f'SUCCESS: Coach for team {team} added or updated.')
		except Exception as e:
			self.log_entry(f'DEEP-ERROR: {e}')
	
	def get_team_statistic(self, season, team, league):
		"""
		Получение статистики команд
		"""
		url = f'https://v3.football.api-sports.io/teams/statistics?season={season}&team={team}&league={league}'
		try:
			data = self._make_api_request(url)
			
			#Обработка ошибок	
			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return
			
			data = data['response']
			league_object = League.objects.get(id=league)
			team_object = Team.objects.get(id=team)
			season_object = Season.objects.get(year=season)
			
			obj, created = TeamStatistic.objects.update_or_create(
				league=league_object,
				team=team_object,
				season=season_object,
				defaults={
					'form': data['form'],
					#Голы забитые по 15-и минуткам ДОМА
					'goal_for_015_total': data['goals']['for']['minute']['0-15']['total'] or 0,
					'goal_for_015_percentage': data['goals']['for']['minute']['0-15']['percentage'] or '0',
					'goal_for_1630_total': data['goals']['for']['minute']['16-30']['total'] or 0,
					'goal_for_1630_percentage': data['goals']['for']['minute']['16-30']['percentage'] or '0',
					'goal_for_3145_total': data['goals']['for']['minute']['31-45']['total'] or 0,
					'goal_for_3145_percentage': data['goals']['for']['minute']['31-45']['percentage'] or '0',
					'goal_for_4660_total': data['goals']['for']['minute']['46-60']['total'] or 0,
					'goal_for_4660_percentage': data['goals']['for']['minute']['46-60']['percentage'] or '0',
					'goal_for_6175_total': data['goals']['for']['minute']['61-75']['total'] or 0,
					'goal_for_6175_percentage': data['goals']['for']['minute']['61-75']['percentage'] or '0',
					'goal_for_7690_total': data['goals']['for']['minute']['76-90']['total'] or 0,
					'goal_for_7690_percentage': data['goals']['for']['minute']['76-90']['percentage'] or '0',
					#Голы забитые по 15-и минуткам ГОСТИ
					'goal_away_015_total': data['goals']['against']['minute']['0-15']['total'] or 0,
					'goal_away_015_percentage': data['goals']['against']['minute']['0-15']['percentage'] or '0',
					'goal_away_1630_total': data['goals']['against']['minute']['16-30']['total'] or 0,
					'goal_away_1630_percentage': data['goals']['against']['minute']['16-30']['percentage'] or '0',
					'goal_away_3145_total': data['goals']['against']['minute']['31-45']['total'] or 0,
					'goal_away_3145_percentage': data['goals']['against']['minute']['31-45']['percentage'] or '0',
					'goal_away_4660_total': data['goals']['against']['minute']['46-60']['total'] or 0,
					'goal_away_4660_percentage': data['goals']['against']['minute']['46-60']['percentage'] or '0',
					'goal_away_6175_total': data['goals']['against']['minute']['61-75']['total'] or 0,
					'goal_away_6175_percentage': data['goals']['against']['minute']['61-75']['percentage'] or '0',
					'goal_away_7690_total': data['goals']['against']['minute']['76-90']['total'] or 0,
					'goal_away_7690_percentage': data['goals']['against']['minute']['76-90']['percentage'] or '0',
					#Карточки жёлтые
					'yellow_015_total': data['cards']['yellow']['0-15']['total'] or 0,
					'yellow_015_percentage': data['cards']['yellow']['0-15']['percentage'] or '0',
					'yellow_1630_total': data['cards']['yellow']['16-30']['total'] or 0,
					'yellow_1630_percentage': data['cards']['yellow']['16-30']['percentage'] or '0',
					'yellow_3145_total': data['cards']['yellow']['31-45']['total'] or 0,
					'yellow_3145_percentage': data['cards']['yellow']['31-45']['percentage'] or '0',
					'yellow_4660_total': data['cards']['yellow']['46-60']['total'] or 0,
					'yellow_4660_percentage': data['cards']['yellow']['46-60']['percentage'] or '0',
					'yellow_6175_total': data['cards']['yellow']['61-75']['total'] or 0,
					'yellow_6175_percentage': data['cards']['yellow']['61-75']['percentage'] or '0',
					'yellow_7690_total': data['cards']['yellow']['76-90']['total'] or 0,
					'yellow_7690_percentage': data['cards']['yellow']['76-90']['percentage'] or '0',
					#Карточки красные
					'red_015_total': data['cards']['red']['0-15']['total'] or 0,
					'red_015_percentage': data['cards']['red']['0-15']['percentage'] or '0',
					'red_1630_total': data['cards']['red']['16-30']['total'] or 0,
					'red_1630_percentage': data['cards']['yellow']['16-30']['percentage'] or '0',
					'red_3145_total': data['cards']['red']['31-45']['total'] or 0,
					'red_3145_percentage': data['cards']['red']['31-45']['percentage'] or '0',
					'red_4660_total': data['cards']['red']['46-60']['total'] or 0,
					'red_4660_percentage': data['cards']['red']['46-60']['percentage'] or '0',
					'red_6175_total': data['cards']['red']['61-75']['total'] or 0,
					'red_6175_percentage': data['cards']['red']['61-75']['percentage'] or '0',
					'red_7690_total': data['cards']['red']['76-90']['total'] or 0,
					'red_7690_percentage': data['cards']['red']['76-90']['percentage'] or '0',
				}
			)
			self.log_entry(f'SUCCESS: Team statistic for team {team} added or updated.')
		except Exception as e:
			self.log_entry(f'DEEP-ERROR: {e}')
			
	def get_all_team_statistic(self):
		"""
		Получить все статистики
		"""
		seasons = 2023
		teams = Team.objects.all()
		for team in teams:
			self.get_team_statistic(seasons, team.id, team.league.first().id)
			
	def get_player_with_stat(self, league, team, season=2023):
		"""
		Получить игроков и их статистику.
		Аттрибуты:
		1)Лига
		2)Команда
		3)Сезон
		"""
		#Запрос к АПИ с выбранными параметрами
		page = 1
		while True:
			url = f'https://v3.football.api-sports.io/players?league={league}&season={season}&team={team}&page={page}'
			
			try:
				data = self._make_api_request(url)
				
				#Обработка ошибок	
				if data['errors']:
					self.log_entry(f'{data["errors"]}')
					return
				elif not data['response']:
					self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
					return
					#Цикл игроков из запроса
					
				for player in data['response']:
					league_object = League.objects.get(id=league)
					season_object = Season.objects.get(year=season)
					team_object = Team.objects.get(id=team)
					
					obj, created = Player.objects.update_or_create(
						id=player['player']['id'],
						defaults = {
							'name': player['player']['name'],
							'team': team_object,
							'first_name': player['player']['firstname'],
							'last_name': player['player']['lastname'],
							'age': player['player']['age'] or 0,
							'birthday': player['player']['birth']['date'] or '',
							'nationality': player['player']['nationality'] or '',
							'height': player['player']['height'] or 0,
							'weight': player['player']['weight'] or 0,
							'photo': player['player']['photo'] or 0,
						}
					)
					self.log_entry(f'SUCCESS: Player {player["player"]["id"]} added or updated.')
					
					player_object = Player.objects.get(id=player['player']['id'])	
					obj_second, created = PlayerStatistic.objects.update_or_create(
						player=player_object,
						season=season_object,
						league=league_object,
						team=team_object,
						defaults = {
							#games
							'appearences': player['statistics'][0]['games']['appearences'] or 0,
							'lineups': player['statistics'][0]['games']['lineups'] or 0,
							'minutes': player['statistics'][0]['games']['minutes'] or 0,
							'number': player['statistics'][0]['games']['number'] or 0,
							'position': player['statistics'][0]['games']['position'] or '',
							'rating': player['statistics'][0]['games']['rating'] or 0.0,
							#sub
							'sub_in': player['statistics'][0]['substitutes']['in'] or 0,
							'sub_out': player['statistics'][0]['substitutes']['out'] or 0,
							'sub_bench': player['statistics'][0]['substitutes']['bench'] or 0,
							#shots
							'shots_total': player['statistics'][0]['shots']['total'] or 0,
							'shots_on': player['statistics'][0]['shots']['on'] or 0,
							#goals
							'goals_total': player['statistics'][0]['goals']['total'] or 0,
							'goals_conceded': player['statistics'][0]['goals']['conceded'] or 0,
							'goals_assists': player['statistics'][0]['goals']['assists'] or 0,
							'goals_saves': player['statistics'][0]['goals']['saves'] or 0,
							#passes
							'passes_total': player['statistics'][0]['passes']['total'] or 0,
							'passes_key': player['statistics'][0]['passes']['key'] or 0,
							'passes_accuracy': player['statistics'][0]['passes']['accuracy'] or 0,
							#tackles
							'tackles_total': player['statistics'][0]['tackles']['total'] or 0,
							'tackles_blocks': player['statistics'][0]['tackles']['blocks'] or 0,
							'tackles_interception': player['statistics'][0]['tackles']['interceptions'] or 0,
							#duels
							'duels_total': player['statistics'][0]['duels']['total'] or 0,
							'duels_won': player['statistics'][0]['duels']['won'] or 0,
							#dribbles
							'dribbles_attempts': player['statistics'][0]['dribbles']['attempts'] or 0,
							'dribbles_success': player['statistics'][0]['dribbles']['success'] or 0,
							'dribbles_past': player['statistics'][0]['dribbles']['past'] or 0,
							#fouls
							'fouls_drawn': player['statistics'][0]['fouls']['drawn'] or 0,
							'fouls_committed': player['statistics'][0]['fouls']['committed'] or 0,
							#cards
							'cards_yellow': player['statistics'][0]['cards']['yellow'] or 0,
							'cards_yellow_red': player['statistics'][0]['cards']['yellowred'] or 0,
							'cards_red': player['statistics'][0]['cards']['red'] or 0,
							#penalty
							'penalty_won': player['statistics'][0]['penalty']['won'] or 0,
							'penalty_committed': player['statistics'][0]['penalty']['commited'] or 0,
							'penalty_scored': player['statistics'][0]['penalty']['scored'] or 0,
							'penalty_missed': player['statistics'][0]['penalty']['missed'] or 0,
							'penalty_saved': player['statistics'][0]['penalty']['saved'] or 0,
						}
					)
					self.log_entry(f'SUCCESS: Player statistic for {player["player"]["id"]} added or updated.')
					
				if data['paging']['current'] < data['paging']['total']:
					page += 1
					self.log_entry(f'SUCCESS: Change page to {page}')
				else:
					break
					
			except Exception as e:
				#Логирование ошибки
				self.log_entry(f'DEEP-ERROR: {e}')
			
	def get_fixture(self, league, season=2023):
		"""
		Получить матчи
		"""
		url = f'https://v3.football.api-sports.io/fixtures?league={league}&season={season}&timezone=Europe/Moscow'
		try:
			data = self._make_api_request(url)
		
		#Обработка ошибок	
			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return
			
			for fixture in data['response']:
				try:
					venue_object = Venue.objects.get(id=fixture['fixture']['venue']['id'])
				except Venue.DoesNotExist:
					venue_object = None

				datetime_obj = parser.parse(fixture['fixture']['date'])

				date_obj = datetime_obj.date()
				time_obj = datetime_obj.time()

				league_object = League.objects.get(id=league)
				season_object = Season.objects.get(year=season)
				team_home_object = Team.objects.get(id=fixture['teams']['home']['id'])
				team_away_object = Team.objects.get(id=fixture['teams']['away']['id'])
				
				obj, created = Fixture.objects.update_or_create(
					id=fixture['fixture']['id'],
					defaults={
						'date': date_obj,
						'time': time_obj,
				        'status': fixture['fixture']['status']['long'] or '',
				        'venue': venue_object,
				        'league': league_object,
				        'season': season_object,
				        'team_home': team_home_object,
				        'team_away': team_away_object,
						'goals_home': fixture['goals']['home'],
						'goals_away': fixture['goals']['away'],
				    }
				)
				self.log_entry(f'SUCCESS: Fixture {fixture["fixture"]["id"]} added or updated.')
		except Exception as e:
			#Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')

	def get_fixture_statistic(self, fixture):
		"""
		Получить статистику матча
		"""
		url = f'https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture}'
		try:
			data = self._make_api_request(url)

			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return

			data = data['response']
			fixture_object = Fixture.objects.get(id=fixture)
			team_home_object = Team.objects.get(id=data[0]['team']['id'])
			team_away_object = Team.objects.get(id=data[1]['team']['id'])

			obj, created = FixtureStatistic.objects.update_or_create(
				fixture=fixture_object,
				team_home=team_home_object,
				away_team=team_away_object,
				defaults={
					'home_on_goal': data[0]['statistics'][0]['value'] or 0,
					'away_on_goal': data[1]['statistics'][0]['value'] or 0,
					'home_off_goal': data[0]['statistics'][1]['value'] or 0,
					'away_off_goal': data[1]['statistics'][1]['value'] or 0,
					'home_total_shots': data[0]['statistics'][2]['value'] or 0,
					'away_total_shots': data[1]['statistics'][2]['value'] or 0,
					'home_blocked_shots': data[0]['statistics'][3]['value'] or 0,
					'away_blocked_shots': data[1]['statistics'][3]['value'] or 0,
					'home_shots_inside_box': data[0]['statistics'][4]['value'] or 0,
					'away_shots_inside_box': data[1]['statistics'][4]['value'] or 0,
					'home_shots_outside_box': data[0]['statistics'][5]['value'] or 0,
					'away_shots_outside_box': data[1]['statistics'][5]['value'] or 0,
					'home_fouls': data[0]['statistics'][6]['value'] or 0,
					'away_fouls': data[1]['statistics'][6]['value'] or 0,
					'home_corner_kicks': data[0]['statistics'][7]['value'] or 0,
					'away_corner_kicks': data[1]['statistics'][7]['value'] or 0,
					'home_offsides': data[0]['statistics'][8]['value'] or 0,
					'away_offsides': data[1]['statistics'][8]['value'] or 0,
					'home_ball_possession': data[0]['statistics'][9]['value'] or '',
					'away_ball_possession': data[1]['statistics'][9]['value'] or '',
					'home_yellow_cards': data[0]['statistics'][10]['value'] or 0,
					'away_yellow_cards': data[1]['statistics'][10]['value'] or 0,
					'home_red_cards': data[0]['statistics'][11]['value'] or 0,
					'away_red_cards': data[1]['statistics'][11]['value'] or 0,
					'home_goalkeeper_saves': data[0]['statistics'][12]['value'] or 0,
					'away_goalkeeper_saves': data[1]['statistics'][12]['value'] or 0,
					'home_total_passes': data[0]['statistics'][13]['value'] or 0,
					'away_total_passes': data[1]['statistics'][13]['value'] or 0,
					'home_passes_accurate': data[0]['statistics'][14]['value'] or 0,
					'away_passes_accurate': data[1]['statistics'][14]['value'] or 0,
					'home_passes_percentage': data[0]['statistics'][15]['value'] or '',
					'away_passes_percentage': data[1]['statistics'][15]['value'] or '',
					'home_expected_goals': data[0]['statistics'][16]['value'] or 0.0,
					'away_expected_goals': data[1]['statistics'][16]['value'] or 0.0,
				}
			)
			self.log_entry(f'SUCCESS: Fixture statistic for fixture {fixture} added or updated.')
		except Exception as e:
			#Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')

	def get_fixture_prediction(self, fixture):
		"""
        Обновить или создать статистику по прогнозу матча
        """
		url = f'https://v3.football.api-sports.io/predictions?fixture={fixture}'  # Замените на реальный адрес API
		try:
			data = self._make_api_request(url)

			if data['errors']:
				self.log_entry(f'{data["errors"]}')
				return
			elif not data['response']:
				self.log_entry(f'SYSTEM-ERROR: Empty response, check the entered parameters. {url}')
				return

			data = data['response'][0]  # Используем [0], так как API возвращает список, но по вашему описанию, вы получаете один элемент
			fixture_object = Fixture.objects.get(id=fixture)
			winner_object = Team.objects.get(id=data['predictions']['winner']['id'])

			obj, created = FixturePrediction.objects.update_or_create(
				fixture=fixture_object,
				defaults={
					'winner': winner_object,
					'winner_comment': data['predictions']['winner']['comment'],
					'under_over': data['predictions']['under_over'],
					'goals_home': float(data['predictions']['goals']['home']),
					'goals_away': float(data['predictions']['goals']['away']),
					'advice': data['predictions']['advice'],
					'percent_home': data['predictions']['percent']['home'],
					'percent_away': data['predictions']['percent']['away'],
					'percent_draw': data['predictions']['percent']['draw'],
					'last_home_form': data['teams']['home']['last_5']['form'],
					'last_away_form': data['teams']['away']['last_5']['form'],
					'last_home_att': data['teams']['home']['last_5']['att'],
					'last_away_att': data['teams']['away']['last_5']['att'],
					'last_home_def': data['teams']['home']['last_5']['def'],
					'last_away_def': data['teams']['away']['last_5']['def'],
					'com_form_home': data['comparison']['form']['home'],
					'com_form_away': data['comparison']['form']['away'],
					'com_att_home': data['comparison']['att']['home'],
					'com_att_away': data['comparison']['att']['away'],
					'com_def_home': data['comparison']['def']['home'],
					'com_def_away': data['comparison']['def']['away'],
					'com_distr_home': data['comparison']['poisson_distribution']['home'],
					'com_distr_away': data['comparison']['poisson_distribution']['away'],
					'com_h2h_home': data['comparison']['h2h']['home'],
					'com_h2h_away': data['comparison']['h2h']['away'],
					'com_goals_home': data['comparison']['goals']['home'],
					'com_goals_away': data['comparison']['goals']['away'],
					'com_total_home': data['comparison']['total']['home'],
					'com_total_away': data['comparison']['total']['away'],
				}
			)
			self.log_entry(f'SUCCESS: Fixture prediction statistic for fixture {fixture} added or updated.')
		except Exception as e:
			# Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')

	def get_all_fixture_statistic(self):
		"""
		Получение всех статистик
		"""
		fix = Fixture.objects.filter(status='Match Finished')
		counter = 0
		for f in fix:
			if counter >= 140:
				self.log_entry(f'PROCCESS: Requests limited. Wait 30 seconds')
				time.sleep(30)
				counter = 0
				self.log_entry(f'SUCCESS: Continue.')
			else:
				self.get_fixture_statistic(f.id)
				counter += 1

	def get_all_fixture_prediction(self):
		"""
		Получить все предсказания
		"""
		match_list = Fixture.objects.exclude(status='Match Finished')
		counter = 0
		for m in match_list:
			if counter >= 140:
				self.log_entry(f'PROCESS: Requests limited. Wait 30 seconds')
				time.sleep(30)
				counter = 0
				self.log_entry(f'SUCCESS: Continue.')
			else:
				self.get_fixture_prediction(m.id)
				counter += 1

	def get_all_player(self, league=None):
		"""
		Получить всех  игроков
		"""
		if league:
			l = League.objects.get(id=league)
			teams = Team.objects.filter(league=l)
			for team in teams:
				self.get_player_with_stat(league, team.id)
		else:		
			leagues = League.objects.all()
			for league in leagues:
				teams = Team.objects.filter(league=league.id)
				for team in teams:
					self.get_player_with_stat(league.id, team.id)
		
	def get_all_team(self):
		"""
		Получить команды всех лиг из БД
		"""
		data = League.objects.all()
		for obj in data:
			self.get_team(obj.id)
			
	def get_all_standings(self):
		"""
		получить таблицы всех лиг
		"""
		data = League.objects.all()
		for obj in data:
			self.get_standings(obj.id)
			
	def get_all_coach(self):
		"""
		Метод для получения всех тренеров
		"""
		teams = Team.objects.all()
		for team in teams:
			self.get_coach(team.id)
			
	def get_all_fixture(self):
		"""
		Получить все матчи
		"""
		leagues = League.objects.all()
		for league in leagues:
			self.get_fixture(league.id)
			
	def get_all(self, date_from, date_to):
		self.get_all_player()
		self.get_all_team()
		self.get_all_standings()
		self.get_all_coach()
		self.get_all_team_statistic()
		self.get_all_fixture(date_from, date_to)