"""
Утилиты для обеспечения системной работы проекта
"""
from datetime import datetime
		
class Logger:
	"""
	Система логирования проекта.
	Сохранение логов в файл: ../logfile.log
	"""
	def log_entry(self, message):
		"""
		Запись лога в файл
		"""
		log_file = '/home/c/cz18656/django_m8aj6/public_html/logs/logfile.log'
		date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with open(log_file, 'a') as file:
			file.write(f'{date}: {message}' + '\n')
	
	
