from django.db import models

# Create your models here.
class Country(models.Model):
	"""
	Countries model
	"""
	name = models.CharField('Название', max_length=16, default='Без названия')
	code = models.CharField('Код страны', max_length=8, default='Без кода')
	flag_url = models.CharField('Ссылка на флаг страны', max_length=64, default='Без флага')
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Страна'
		verbose_name_plural = 'Страны'
		

class Season(models.Model):
	"""
	Seasons model
	"""
	year = models.IntegerField('Год сезона', primary_key=True)
	
	def __str__(self):
		return str(self.year)
		
	class Meta:
		verbose_name = 'Сезон'
		verbose_name_plural = 'Сезоны'
		
		
class League(models.Model):
	"""
	Leagues model
	"""
	#RELATED FIELDS
	country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна')
	season = models.ForeignKey('Season', on_delete=models.CASCADE, verbose_name='Сезон')
	#SIMPLE FIELDS
	id = models.IntegerField('ID', primary_key=True)
	name = models.CharField('Название', max_length=64, default='Без названия')
	logo_url = models.CharField('Ссылка на логотип лиги', max_length=64, default='Без логотипа')
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Лига'
		verbose_name_plural = 'Лиги'
		

class Venue(models.Model):
	"""
	Venues model
	"""
	id = models.IntegerField('ID', primary_key=True)
	name = models.CharField('Название', max_length=64, default='Без имени')
	address = models.CharField('Адресс', max_length=128, default='Без адресса')
	city = models.CharField('Город', max_length=64, default='Без города')
	surface = models.CharField('Покрытие', max_length=64, default='Без покрытия')
	capacity = models.IntegerField('Вместительность', default=0)
	image = models.CharField('Ссылка на фото', max_length=128, default='Без фото')
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Стадион'
		verbose_name_plural = 'Стадионы'
	
	
class Team(models.Model):
	"""
	Teams model
	"""
	#RELATED FIELDS
	country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна')
	season = models.ForeignKey('Season', on_delete=models.CASCADE, verbose_name='Сезон')
	league = models.ManyToManyField('League', verbose_name='Лига')
	venue = models.ForeignKey('Venue', on_delete=models.CASCADE, verbose_name='Стадион')
	#SIMPLE FIELDS
	id = models.IntegerField('ID', primary_key=True)
	name = models.CharField('Название', max_length=64, default='Без названия')
	code = models.CharField('Код команды', max_length=8, null=True, blank=True)
	logo_url = models.CharField('Ссылка на логотип команды', max_length=64, default='Без логотипа')
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Команда'
		verbose_name_plural = 'Команды'
		
		
class LeagueTable(models.Model):
	"""
	League table model
	"""
	#RELATED FIELDS
	league = models.ForeignKey('League', on_delete=models.CASCADE, verbose_name='Лига')
	team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Команда')
	#SIMPLE FIELDS
	position = models.PositiveIntegerField('Позиция', default=0)
	points = models.PositiveIntegerField('Очки', default=0)
	form = models.CharField('Форма', max_length=64, default='')
	#FULL STAT
	played = models.PositiveIntegerField('Всего игр', default=0)
	win = models.PositiveIntegerField('Победа', default=0)
	draw = models.PositiveIntegerField('Ничья', default=0)
	lose = models.PositiveIntegerField('Поражение', default=0)
	goal_for = models.PositiveIntegerField('Забитых мячей', default=0)
	goal_against = models.PositiveIntegerField('Пропущенных мячей', default=0)
	#HOME STAT
	played_home = models.PositiveIntegerField('Всего игр дома', default=0)
	win_home = models.PositiveIntegerField('Победа дома', default=0)
	draw_home = models.PositiveIntegerField('Ничья дома', default=0)
	lose_home = models.PositiveIntegerField('Поражение дома', default=0)
	goal_for_home = models.PositiveIntegerField('Забитых мячей дома', default=0)
	goal_against_home = models.PositiveIntegerField('Пропущенных мячей дома', default=0)
	#AWAY STAT
	played_away = models.PositiveIntegerField('Всего игр в гостях', default=0)
	win_away = models.PositiveIntegerField('Победа в гостях', default=0)
	draw_away = models.PositiveIntegerField('Ничья в гостях', default=0)
	lose_away = models.PositiveIntegerField('Поражение в гостях', default=0)
	goal_for_away = models.PositiveIntegerField('Забитых мячей в гостях', default=0)
	goal_against_away = models.PositiveIntegerField('Пропущенных мячей в гостях', default=0)
	
	def __str__(self):
		return str(self.league)
	
	class Meta:
		verbose_name = 'Таблица'
		verbose_name_plural = 'Таблицы'
		
		
class Player(models.Model):
	"""
	Players model
	"""
	id = models.IntegerField('ID', primary_key=True)
	name = models.CharField('Полное имя', null=True, blank=True, max_length=32, default='')
	team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Команда')
	first_name = models.CharField('Имя', max_length=32, null=True, blank=True, default='')
	last_name = models.CharField('Фамилия', max_length=32, null=True, blank=True, default='')
	age = models.IntegerField('Возраст', null=True, blank=True, default=0)
	birthday = models.CharField('День рождения', max_length=32, null=True, blank=True, default='')
	nationality = models.CharField('Национальность', max_length=32, null=True, blank=True, default='')
	height = models.CharField('Рост', max_length=32, null=True, blank=True, default='')
	weight = models.CharField('Вес', max_length=32, null=True, blank=True, default='')
	photo = models.CharField('Ссылка на фото', max_length=128, null=True, blank=True, default='')
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Игрок'
		verbose_name_plural = 'Игроки'
		
		
class PlayerStatistic(models.Model):
	"""
	Player statistic model
	"""
	player = models.ForeignKey('Player', on_delete=models.CASCADE, verbose_name='Игрок')
	league = models.ForeignKey('League', on_delete=models.CASCADE, verbose_name='Лига')
	team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Команда')
	season = models.ForeignKey('Season', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сезон')
	#games
	appearences = models.IntegerField('Количество появлений на поле', null=True, blank=True)
	lineups = models.IntegerField('Количество появлений в стартовом составе', null=True, blank=True)
	minutes = models.IntegerField('Количество минут на поле', null=True, blank=True)
	number = models.IntegerField('Номер игрока', null=True, blank=True)
	position = models.CharField('Позиция игрока', max_length=32, null=True, blank=True)
	rating = models.FloatField('Рейтинг игрока', null=True, blank=True)
	#substitutes
	sub_in = models.IntegerField('Выходов на замену', null=True, blank=True)
	sub_out = models.IntegerField('Был заменён', null=True, blank=True)
	sub_bench = models.IntegerField('На скамейке', null=True, blank=True)
	#shots
	shots_total = models.IntegerField('Ударов', null=True, blank=True)
	shots_on = models.IntegerField('Ударов в створ', null=True, blank=True)
	#goals
	goals_total = models.IntegerField('Голов', null=True, blank=True)
	goals_assists = models.IntegerField('Голевых передач', null=True, blank=True)
	goals_conceded = models.IntegerField('Пропущенных голов', null=True, blank=True)
	goals_saves = models.IntegerField('Сэйвов', null=True, blank=True)
	#passes
	passes_total = models.IntegerField('Передач', null=True, blank=True)
	passes_key = models.IntegerField('Ключевых передач', null=True, blank=True)
	passes_accuracy = models.FloatField('Процент точных передач', null=True, blank=True)
	#tackles
	tackles_total = models.IntegerField('Количество отборов', null=True, blank=True)
	tackles_blocks = models.IntegerField('Блокированных мячей', null=True, blank=True)
	tackles_interception = models.IntegerField('Количество перехватов', null=True, blank=True)
	#duels
	duels_total = models.IntegerField('Количество единоборств', null=True, blank=True)
	duels_won = models.IntegerField('Удачных единоборств', null=True, blank=True)
	#dribbles
	dribbles_attempts = models.IntegerField('Попыток дриблинга', null=True, blank=True)
	dribbles_success = models.IntegerField('Успешных дриблингов', null=True, blank=True)
	dribbles_past = models.IntegerField('Игроков обыгранных в дриблинге', null=True, blank=True)
	#fouls
	fouls_drawn = models.IntegerField('Заработанных фолов', null=True, blank=True)
	fouls_committed = models.IntegerField('Совершённых фолов', null=True, blank=True)
	#cards
	cards_yellow = models.IntegerField('Жёлтых карточек', null=True, blank=True)
	cards_yellow_red = models.IntegerField('Двойных жёлтых карточек', null=True, blank=True)
	cards_red = models.IntegerField('Красных карточек', null=True, blank=True)
	#penalty
	penalty_won = models.IntegerField('Заработанных пенальти', null=True, blank=True)
	penalty_committed = models.IntegerField('Нарушений в штрафной', null=True, blank=True)
	penalty_scored = models.IntegerField('Забитых пенальти', null=True, blank=True)
	penalty_missed = models.IntegerField('Не забитых пенальти', null=True, blank=True)
	penalty_saved = models.IntegerField('Отбитых пенальти', null=True, blank=True)
	
	def __str__(self):
		return str(self.player)
		
	class Meta:
		verbose_name = 'Статистика игрока'
		verbose_name_plural = 'Статистики игроков'


class Coach(models.Model):
	"""
	Model for coach
	"""
	#RELATED FIELDS
	team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Команда')
	#SIMPLE FIELDS
	id = models.IntegerField('ID', primary_key=True)
	name = models.CharField('Полное имя', null=True, blank=True, max_length=32, default='Без имени')
	first_name = models.CharField('Имя', null=True, blank=True, max_length=32, default='Без имени')
	last_name = models.CharField('Фамилия', null=True, blank=True, max_length=32, default='Без имени')
	age = models.IntegerField('Возраст', null=True, blank=True, default=0)
	birthday = models.CharField('День рождения', max_length=32, default='dd-mm-yyyy')
	nationality = models.CharField('Национальность', max_length=32, null=True, blank=True, default='')
	height = models.CharField('Рост', max_length=32, null=True, blank=True, default='')
	weight = models.CharField('Вес', max_length=32, null=True, blank=True, default='')
	photo = models.CharField('Ссылка на фото', max_length=128, null=True, blank=True, default='')
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name = 'Тренер'
		verbose_name_plural = 'Тренеры'


class TeamStatistic(models.Model):
	"""
	Model for TeamStatistic
	"""
	#RELATED FIELDS
	league = models.ForeignKey('League', on_delete=models.CASCADE, verbose_name='Лига')
	team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Команда')
	season = models.ForeignKey('Season', on_delete=models.CASCADE, verbose_name='Сезон')
	form = models.CharField('Форма', max_length=50, default='')
	#
	goal_for_015_total = models.IntegerField('Голов с 0 по 15 минуты', default=0)
	goal_for_015_percentage = models.CharField('Голов с 0 по 15 минуты', max_length=50, default='')
	goal_for_1630_total = models.IntegerField('Голов с 16 по 30 минуты', default=0)
	goal_for_1630_percentage = models.CharField('Голов с 16 по 30 минуты', max_length=50, default='')
	goal_for_3145_total = models.IntegerField('Голов с 31 по 45 минуты', default=0)
	goal_for_3145_percentage = models.CharField('Голов с 31 по 45 минуты', max_length=50, default='')
	goal_for_4660_total = models.IntegerField('Голов с 46 по 60 минуты', default=0)
	goal_for_4660_percentage = models.CharField('Голов с 46 по 60 минуты', max_length=50, default='')
	goal_for_6175_total = models.IntegerField('Голов с 61 по 75 минуты', default=0)
	goal_for_6175_percentage = models.CharField('Голов с 61 по 75 минуты', max_length=50, default='')
	goal_for_7690_total = models.IntegerField('Голов с 76 по 90 минуты', default=0)
	goal_for_7690_percentage = models.CharField('Голов с 76 по 90 минуты', max_length=50, default='')
	#
	goal_away_015_total = models.IntegerField('Голов с 0 по 15 минуты', default=0)
	goal_away_015_percentage = models.CharField('Голов с 0 по 15 минуты', max_length=50, default='')
	goal_away_1630_total = models.IntegerField('Голов с 16 по 30 минуты', default=0)
	goal_away_1630_percentage = models.CharField('Голов с 16 по 30 минуты', max_length=50, default='')
	goal_away_3145_total = models.IntegerField('Голов с 16 по 30 минуты', default=0)
	goal_away_3145_percentage = models.CharField('Голов с 31 по 45 минуты', max_length=50, default='')
	goal_away_4660_total = models.IntegerField('Голов с 31 по 45 минуты', default=0)
	goal_away_4660_percentage = models.CharField('Голов с 46 по 60 минуты', max_length=50, default='')
	goal_away_6175_total = models.IntegerField('Голов с 46 по 60 минуты', default=0)
	goal_away_6175_percentage = models.CharField('Голов с 61 по 75 минуты', max_length=50, default='')
	goal_away_7690_total = models.IntegerField('Голов с 76 по 90 минуты', default=0)
	goal_away_7690_percentage = models.CharField('Голов с 76 по 90 минуты', max_length=50, default='')
	#
	yellow_015_total = models.IntegerField('Жёлтых с 0 по 15 минуты', default=0)
	yellow_015_percentage = models.CharField('Жёлтых с 0 по 15 минуты', max_length=50, default='')
	yellow_1630_total = models.IntegerField('Жёлтых с 16 по 30 минуты', default=0)
	yellow_1630_percentage = models.CharField('Жёлтых с 16 по 30 минуты', max_length=50, default='')
	yellow_3145_total = models.IntegerField('Жёлтых с 31 по 45 минуты', default=0)
	yellow_3145_percentage = models.CharField('Жёлтых с 31 по 45 минуты', max_length=50, default='')
	yellow_4660_total = models.IntegerField('Жёлтых с 46 по 60 минуты', default=0)
	yellow_4660_percentage = models.CharField('Жёлтых с 46 по 60 минуты', max_length=50, default='')
	yellow_6175_total = models.IntegerField('Жёлтых с 61 по 75 минуты', default=0)
	yellow_6175_percentage = models.CharField('Жёлтых с 61 по 75 минуты', max_length=50, default='')
	yellow_7690_total = models.IntegerField('Жёлтых с 76 по 90 минуты', default=0)
	yellow_7690_percentage = models.CharField('Жёлтых с 76 по 90 минуты', max_length=50, default='')
	#
	red_015_total = models.IntegerField('Красных с 0 по 15 минуты', default=0)
	red_015_percentage = models.CharField('Красных с 0 по 15 минуты', max_length=50, default='')
	red_1630_total = models.IntegerField('Красных с 16 по 30 минуты', default=0)
	red_1630_percentage = models.CharField('Красных с 16 по 30 минуты', max_length=50, default='')
	red_3145_total = models.IntegerField('Красных с 31 по 45 минуты', default=0)
	red_3145_percentage = models.CharField('Красных с 31 по 45 минуты', max_length=50, default='')
	red_4660_total = models.IntegerField('Красных с 46 по 60 минуты', default=0)
	red_4660_percentage = models.CharField('Красных с 46 по 60 минуты', max_length=50, default='')
	red_6175_total = models.IntegerField('Красных с 61 по 75 минуты', default=0)
	red_6175_percentage = models.CharField('Красных с 61 по 75 минуты', max_length=50, default='')
	red_7690_total = models.IntegerField('Красных с 76 по 90 минуты', default=0)
	red_7690_percentage = models.CharField('Красных с 76 по 90 минуты', max_length=50, default='')
	
	def __str__(self):
		return str(self.team)
		
	class Meta:
		verbose_name = 'Статистика команды'
		verbose_name_plural = 'Статистики команд'
		
		
class Fixture(models.Model):
	"""
	Model for fixturies
	"""
	id = models.IntegerField('ID', primary_key=True)
	date = models.DateField('Дата матча', null=True, blank=True)
	time = models.TimeField('Время матча', null=True, blank=True)
	venue = models.ForeignKey('Venue', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Стадион')
	season = models.ForeignKey('Season', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сезон')
	league = models.ForeignKey('League', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Лига')
	team_home = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_fixtures', verbose_name='Домашняя команда')
	team_away = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_fixtures', verbose_name='Гостевая команда')
	status = models.CharField('Статус', max_length=50, null=True, blank=True, default='')
	goals_home = models.IntegerField('Голов домашней команды', null=True, blank=True, default=0)
	goals_away = models.IntegerField('Голов гостевой команды', null=True, blank=True, default=0)
	
	def __str__(self):
		return f'{self.team_home} x {self.team_away}'
		
	class Meta:
		verbose_name = 'Матч'
		verbose_name_plural = 'Матчи'


class FixtureStatistic(models.Model):
	"""
	Model for match statistic
	"""
	fixture = models.ForeignKey('Fixture', on_delete=models.CASCADE, verbose_name='Матч')
	team_home = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_fixture_statistic')
	away_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_fixture_statistic')

	# HOME
	home_on_goal = models.IntegerField('Ударов в створ', default=0)
	home_off_goal = models.IntegerField('Ударов мимо ворот', default=0)
	home_total_shots = models.IntegerField('Всего ударов', default=0)
	home_blocked_shots = models.IntegerField('Заблокированные удары', default=0)
	home_shots_inside_box = models.IntegerField('Удары внутри штрафной площади', default=0)
	home_shots_outside_box = models.IntegerField('Удары за пределами штрафной площади', default=0)
	home_fouls = models.IntegerField('Фолы', default=0)
	home_corner_kicks = models.IntegerField('Угловые удары', default=0)
	home_offsides = models.IntegerField('Офсайды', default=0)
	home_ball_possession = models.CharField('Владение мячом', max_length=5, null=True, blank=True)
	home_yellow_cards = models.IntegerField('Желтые карточки', default=0)
	home_red_cards = models.IntegerField('Красные карточки', null=True, blank=True)
	home_goalkeeper_saves = models.IntegerField('Сейвы вратаря', default=0)
	home_total_passes = models.IntegerField('Всего пасов', default=0)
	home_passes_accurate = models.IntegerField('Точные пасы', default=0)
	home_passes_percentage = models.CharField('Процент точных пасов', max_length=5, null=True, blank=True)
	home_expected_goals = models.FloatField('Ожидаемые голы', null=True, blank=True)

	# AWAY
	away_on_goal = models.IntegerField('Ударов в створ', default=0)
	away_off_goal = models.IntegerField('Ударов мимо ворот', default=0)
	away_total_shots = models.IntegerField('Всего ударов', default=0)
	away_blocked_shots = models.IntegerField('Заблокированные удары', default=0)
	away_shots_inside_box = models.IntegerField('Удары внутри штрафной площади', default=0)
	away_shots_outside_box = models.IntegerField('Удары за пределами штрафной площади', default=0)
	away_fouls = models.IntegerField('Фолы', default=0)
	away_corner_kicks = models.IntegerField('Угловые удары', default=0)
	away_offsides = models.IntegerField('Офсайды', default=0)
	away_ball_possession = models.CharField('Владение мячом', max_length=5, null=True, blank=True)
	away_yellow_cards = models.IntegerField('Желтые карточки', default=0)
	away_red_cards = models.IntegerField('Красные карточки', null=True, blank=True)
	away_goalkeeper_saves = models.IntegerField('Сейвы вратаря', default=0)
	away_total_passes = models.IntegerField('Всего пасов', default=0)
	away_passes_accurate = models.IntegerField('Точные пасы', default=0)
	away_passes_percentage = models.CharField('Процент точных пасов', max_length=5, null=True, blank=True)
	away_expected_goals = models.FloatField('Ожидаемые голы', null=True, blank=True)

	def __str__(self):
		return f"{self.team_home} vs. {self.away_team} Statistic"

	class Meta:
		verbose_name = 'Статистика матча'
		verbose_name_plural = 'Статистики матчей'


class FixturePrediction(models.Model):
	"""
	Model for fixture prediction
	"""
	fixture = models.ForeignKey('Fixture', on_delete=models.CASCADE, verbose_name='Матч')
	winner = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Победитель')
	winner_comment = models.CharField('Комментарий победителю', max_length=32, null=True, blank=True)
	under_over = models.CharField('ТБ/ТМ', max_length=32, null=True, blank=True)
	goals_home = models.FloatField('Тотал Д', null=True, blank=True)
	goals_away = models.FloatField('Тотал Г', null=True, blank=True)
	advice = models.CharField('Предикт', max_length=128, null=True, blank=True)
	percent_home = models.CharField('Шанс домашней', max_length=10, null=True, blank=True)
	percent_away = models.CharField('Шанс гостевой', max_length=10, null=True, blank=True)
	percent_draw = models.CharField('Шанс ничьи', max_length=10, null=True, blank=True)

	last_home_form = models.CharField('Форма 5 дома', max_length=10, null=True, blank=True)
	last_away_form = models.CharField('Форма 5 гости', max_length=10, null=True, blank=True)
	last_home_att = models.CharField('Атака 5 дома', max_length=10, null=True, blank=True)
	last_away_att = models.CharField('Атака 5 гости', max_length=10, null=True, blank=True)
	last_home_def = models.CharField('Защита 5 дома', max_length=10, null=True, blank=True)
	last_away_def = models.CharField('Защита 5 гости', max_length=10, null=True, blank=True)

	com_form_home = models.CharField('Форма бар дома', max_length=10, null=True, blank=True)
	com_form_away = models.CharField('Форма бар гости', max_length=10, null=True, blank=True)
	com_att_home = models.CharField('Атака бар дома', max_length=10, null=True, blank=True)
	com_att_away = models.CharField('Атака бар гости', max_length=10, null=True, blank=True)
	com_def_home = models.CharField('Защита бар дома', max_length=10, null=True, blank=True)
	com_def_away = models.CharField('Зашита бар гости', max_length=10, null=True, blank=True)
	com_distr_home = models.CharField('Паусон бар дом', max_length=10, null=True, blank=True)
	com_distr_away = models.CharField('Паусон бар гости', max_length=10, null=True, blank=True)
	com_h2h_home = models.CharField('h2h бар дом', max_length=10, null=True, blank=True)
	com_h2h_away = models.CharField('h2h бар гости', max_length=10, null=True, blank=True)
	com_goals_home = models.CharField('Голы бар дома', max_length=10, null=True, blank=True)
	com_goals_away = models.CharField('Голы бар гости', max_length=10, null=True, blank=True)
	com_total_home = models.CharField('Общее бар дома', max_length=10, null=True, blank=True)
	com_total_away = models.CharField('Общее бар гости', max_length=10, null=True, blank=True)

	def __str__(self):
		return 'pred'

	class Meta:
		verbose_name = 'Предсказание матча'
		verbose_name_plural = 'Предсказания матчей'