from core.utils import Logger
from core.data import YAPIClient
from celery import Celery
app = Celery('football')
a = YAPIClient()
l = Logger()

@app.task(ignore_result=False)
def standings_task():
    try:
        a.get_all_standings()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")

@app.task(ignore_result=False)
def player_task():
    l.log_entry("Задача pr-try")
    try:
        l.log_entry("Задача try")
        a.get_all_player()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")

@app.task(ignore_result=False)
def coach_task():
    l.log_entry("Задача pr-try")
    try:
        l.log_entry("Задача try")
        a.get_all_coach()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")

@app.task(ignore_result=False)
def team_statistic_task():
    l.log_entry("Задача pr-try")
    try:
        l.log_entry("Задача try")
        a.get_all_team_statistic()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")

@app.task(ignore_result=False)
def fixture_task():
    l.log_entry("Задача pr-try")
    try:
        l.log_entry("Задача try")
        a.get_all_fixture()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")

@app.task(ignore_result=False)
def fixture_statistic_task():
    l.log_entry("Задача pr-try")
    try:
        l.log_entry("Задача try")
        a.get_all_fixture_statistic()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")

@app.task(ignore_result=False)
def fixture_predict_task():
    l.log_entry("Задача pr-try")
    try:
        l.log_entry("Задача try")
        a.get_all_fixture_prediction()
        l.log_entry("Задача выполнена")
    except Exception as e:
        l.log_entry(f"Ошибка в задаче: {e}")