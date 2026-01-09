from django.contrib import admin
from .models import Round, Hand
#
# class HandsInLine(admin.TabularInline):
#     model = Hand
#     extra = 0
#
# class DeckAdmin(admin.ModelAdmin):
#     inlines = [HandsInLine]
#
# admin.site.register(Round, DeckAdmin)