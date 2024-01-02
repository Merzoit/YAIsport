from core.models import *
from site1.settings import API_KEY, API_KEY2
import requests
import json
import time
import os
from site1.settings import BASE_DIR
from datetime import datetime
from core.utils import Logger

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
				country_object = Country.objects.get(name=team['team']['country'])
				season_object = Season.objects.get(year=season)
				league_object = League.objects.get(id=league)
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
			
			coach = data['response'][0]
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
			self.get_team_statistic(seasons, team.id, team.league.id)
			
	def get_player_with_stat(self, league, team, season=2023):
		"""
		Получить игроков и их статистику.
		Аттрибуты:
		1)Лига
		2)Команда
		3)Сезон
		"""
		#Запрос к АПИ с выбранными параметрами
		url = f'https://v3.football.api-sports.io/players?league={league}&season={season}&team={team}'
		
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
						'first_name': player['player']['firstname'],
						'last_name': player['player']['lastname'],
						'age': player['player']['age'],
						'birthday': player['player']['birth']['date'],
						'nationality': player['player']['nationality'],
						'height': player['player']['height'],
						'weight': player['player']['weight'],
						'photo': player['player']['photo'],
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
		except Exception as e:
			#Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')
			
	def get_fixture(self, league, date_from, date_to, season=2023):
		"""
		Получить матчи
		"""
		url = f'https://v3.football.api-sports.io/fixtures?league={league}&season={season}&from={date_from}&to={date_to}&timezone=Europe/Moscow'
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
    				
				league_object = League.objects.get(id=league)
				season_object = Season.objects.get(year=season)
				team_home_object = Team.objects.get(id=fixture['teams']['home']['id'])
				team_away_object = Team.objects.get(id=fixture['teams']['away']['id'])
				
				obj, created = Fixture.objects.update_or_create(
					id=fixture['fixture']['id'],
					defaults={
						'date': fixture['fixture']['date'] or '',
				        'status': fixture['fixture']['status']['long'] or '',
				        'venue': venue_object,
				        'league': league_object,
				        'season': season_object,
				        'team_home': team_home_object,
				        'team_away': team_away_object,
				    }
				)
				self.log_entry(f'SUCCESS: Fixture {fixture["fixture"]["id"]} added or updated.')
		except Exception as e:
			#Логирование ошибки
			self.log_entry(f'DEEP-ERROR: {e}')
			
	def get_all_player(self):
		"""
		Получить всех  игроков
		"""
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
			
	def get_all_fixture(self, date_from, date_to):
		"""
		Получить все матчи
		"""
		leagues = League.objects.all()
		for league in leagues:
			self.get_fixture(league.id, date_from, date_to)
			
	def get_all(self, date_from, date_to):
		self.get_all_player()
		self.get_all_team()
		self.get_all_standings()
		self.get_all_coach()
		self.get_all_team_statistic()
		self.get_all_fixture(date_from, date_to)