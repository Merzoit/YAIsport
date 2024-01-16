from django.contrib import admin

from .models import *

admin.site.register(Country)
admin.site.register(Season)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Venue)
admin.site.register(LeagueTable)
admin.site.register(Player)
admin.site.register(PlayerStatistic)
admin.site.register(Coach)
admin.site.register(TeamStatistic)
admin.site.register(Fixture)
admin.site.register(FixtureStatistic)
admin.site.register(FixturePrediction)
