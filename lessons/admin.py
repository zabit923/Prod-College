from django.contrib import admin
from django import forms
from .models import Lecture, Schedules, RPD



@admin.register(Schedules)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('facult', 'course')


@admin.register(Lecture)
class Lecture(admin.ModelAdmin):
    list_display = ('title',)


