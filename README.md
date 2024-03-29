# YAISport

**YAISport** - это проект, предоставляющий статистику, анализ и предсказания исходов спортивных событий с использованием методов искусственного интеллекта.

Данные получены через API: [API Football](https://www.api-football.com/).

## Структура проекта
Проект организован в несколько основных директорий:

### core/
Содержит основную логику приложения:
- `templates/` - HTML-шаблоны, включая вложенные шаблоны в `include/`.
- `admin.py` - настройки административного интерфейса Django.
- `apps.py` - конфигурация приложения core.
- `data.py` - класс `YAIclient` для обработки данных и записи их в БД.
- `models.py` - модели Django для приложения core.
- `urls.py` - маршруты URL для приложения core.
- `utils.py` - вспомогательные функции, включая логирование.

### logs/
Хранит логи проекта:
- `logfile.log` - основной файл журнала.

### site1/
Конфигурация всего проекта:
- `asgi.py` - асинхронный интерфейс сервера.
- `wsgi.py` - интерфейс сервера для веб-приложений.
- `settings.py` - настройки Django для проекта.
- `urls.py` - глобальные маршруты URL проекта.

### static/
Статические файлы проекта:
- `css/` - стили CSS.
- `images/` - изображения для проекта.
- `admin/` - статические файлы для админки Django.

### Корневой каталог
- `manage.py` - утилита командной строки Django для управления проектом.

## Схемы и Диаграммы
**Схема БД проекта:**
![Схема БД проекта](archi-beta.jpg)

**Диаграмма БД проекта:**
![Диаграмма БД проекта](dbdiagramm.png)
Просмотреть диаграмму можно по ссылке: [dbdiagram.io](https://dbdiagram.io/d/65943cdeac844320ae1ce171)

## Описание проекта
Проект включает следующие ключевые модели и их описание:
- `Country` - страны, участвующие в лигах.
- `Season` - сезоны, для которых доступны данные.
- `League` - лиги в рамках проекта.
- `Team` - команды в лигах.
- `Player` - игроки команд.
- `Venue` - стадионы, на которых проходят матчи.
- `LeagueTable` - результаты лиг.
- `PlayerStatistic` - статистика игроков.
- `Coach` - тренеры команд.
- `TeamStatistic` - статистика команд.
- `Fixture` - матчи и события.

## Логирование
- `DEEP-ERROR` - логирование необработанных исключений.
- `SYSTEM-ERROR` - логирование обработанных ошибок.
- `SUCCESS` - записи об успешных операциях.

## Методы класса YAIclient в data.py
Класс `YAIclient` отвечает за взаимодействие с API и запись данных в базу данных проекта. Вот описание его ключевых методов:

- `_make_api_request(url)`: Приватный метод, принимающий URL-адрес эндпоинта API и возвращающий данные в формате JSON.
- `get_league(country, season)`: Получает данные о спортивных лигах, принимает `country` (страна) и `season` (сезон).
- `get_standings(league, season)`: Получает турнирную таблицу лиги, принимает `league` (лига) и `season` (сезон).
- `get_team(league, season)`: Получает данные о командах, принимает `league` (лига) и `season` (сезон), и включает встроенный метод для получения данных стадиона `Venue`.
- `get_coach(team)`: Получает информацию о тренерах команд, принимает `team` (команда).
- `get_team_statistic(season, team, league)`: Получает статистику команды за сезон, принимает `season` (сезон), `team` (команда) и `league` (лига).
- `get_player_with_stat(league, team, season)`: Получает данные об игроках и их статистику, принимает `league` (лига), `team` (команда) и `season` (сезон).
- `get_fixture(league, date_from, date_to, season)`: Получает список матчей за определенный период, принимает `league` (лига), `date_from` и `date_to` (даты начала и конца периода) и `season` (сезон).
- `get_all_...()`: Методы для получения или обновления данных всех доступных в БД стран, лиг и т.д.
- `get_all()`: Метод для последовательного обновления данных по всей базе данных проекта.

Все методы класса `YAIclient` предназначены для внутреннего использования и не возвращают значения напрямую, вместо этого они записывают результаты своей работы непосредственно в базу данных.
