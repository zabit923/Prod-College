from django.contrib import admin
from django import forms
from .models import Lecture, Schedules, RPD
from ckeditor_uploader.widgets import CKEditorUploadingWidget




class LectureAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Lecture
        fields = '__all__'


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title',)
    form = LectureAdminForm


@admin.register(Schedules)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('facult',)


@admin.register(RPD)
class RPDAdmin(admin.ModelAdmin):
    list_display = ('course',)
