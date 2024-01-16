from django.db.models import Sum
from copy import deepcopy
from .models import *
class YAIalgorythm:

	def team_statistic(self, team_id):
		team = Team.objects.get(id=team_id)
		statistics = FixtureStatistic.objects.filter(team_home=team) | FixtureStatistic.objects.filter(away_team=team)

		initial_stats = {
			'Ударов в створ': 0,
			'Ударов мимо ворот': 0,
			'Всего ударов': 0,
			'Заблокированные удары': 0,
			'Удары из штрафной': 0,
			'Удары из-за штрафной': 0,
			'Фолы': 0,
			'Угловые': 0,
			'Офсайды': 0,
			'Желтые карточки': 0,
			'Красные карточки': 0,
			'Сейвы вратаря': 0,
			'Всего пасов': 0,
			'Точные пасы': 0,
			'Ожидаемые голы': 0.0,
		}

		stat_translations = {
			'Ударов в створ': 'on_goal',
			'Ударов мимо ворот': 'off_goal',
			'Всего ударов': 'total_shots',
			'Заблокированные удары': 'blocked_shots',
			'Удары из штрафной': 'shots_inside_box',
			'Удары из-за штрафной': 'shots_outside_box',
			'Фолы': 'fouls',
			'Угловые': 'corner_kicks',
			'Офсайды': 'offsides',
			'Желтые карточки': 'yellow_cards',
			'Красные карточки': 'red_cards',
			'Сейвы вратаря': 'goalkeeper_saves',
			'Всего пасов': 'total_passes',
			'Точные пасы': 'passes_accurate',
			'Ожидаемые голы': 'expected_goals',
		}

		home_stat = {'for': deepcopy(initial_stats), 'against': deepcopy(initial_stats)}
		away_stat = {'for': deepcopy(initial_stats), 'against': deepcopy(initial_stats)}

		for obj in statistics:
			side = 'home' if obj.team_home == team else 'away'
			opposite_side = 'away' if side == 'home' else 'home'

			for key in initial_stats:
				if side == 'home':
					home_stat['for'][key] += getattr(obj, f"{side}_{stat_translations[key]}", 0)
					home_stat['against'][key] += getattr(obj, f"{opposite_side}_{stat_translations[key]}", 0)
				else:
					away_stat['for'][key] += getattr(obj, f"{side}_{stat_translations[key]}", 0)
					away_stat['against'][key] += getattr(obj, f"{opposite_side}_{stat_translations[key]}", 0)

			total = {
				'for': {key: home_stat['for'][key] + away_stat['for'][key] for key in initial_stats},
				'against': {key: home_stat['against'][key] + away_stat['against'][key] for key in initial_stats},
			}

		return {
			'home_stat': home_stat,
			'away_stat': away_stat,
			'total': total
		}
