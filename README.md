YAISport - проект, содержащий статистику по спортивным событиям, их анализ и предсказания исходов событий и прочих статистических результатов при помощи анализа искуственного интелекта.

Получение данных по средствам API. https://www.api-football.com/

# YAISport
Навигация.
- **core/**
  - templates/
    - include/
  - admin.py
  - apps.py
  - data.py
  - models.py
  - urls.py
  - utils.py
  - urls.py

- **logs/**
  - logfile.log

- **site1/**
  - asgi.py
  - wsgi.py
  - settings.py
  - urls.py

- **static/**
  - css/
  - image/
  - admin/

- manage.py

1) Core - содержит основную логику приложения.
   а) templates - содержит шаблоны формата HTML, имеет вложенную папку **include**, содержащую вложенные шаблоны.
   б) admin.py - конфигурация для интерфейса панели администрирования Django.
   в) apps.py - конфигурация для приложения **core**.
   г) data.py - содержит класс YAIclient, модуль для обработки задач, связанных с данными. Основная задача - запись данных в БД через API.
     Методы YAIclient:
     **_make_api_request(url)** - метод принимает аргументом эндпоинт для получения данных, возвращает данные в формате json.
     **get_league(country, season)** - метод для получения данных о спортивной лиге. Принимает аргументы **country** страна, **season** сезон.
     Метод ничего не возвращает, производит запись из полученных данных в БД проекта.
