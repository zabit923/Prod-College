from django.contrib import admin
from django import forms
from .models import Lecture, Schedules, RPD, ProfDB, Reviews


@admin.register(Schedules)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('facult',)


@admin.register(Lecture)
class Lecture(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(ProfDB)
class ProfDB(admin.ModelAdmin):
    list_display = ('facult', 'link')


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'lecture')

