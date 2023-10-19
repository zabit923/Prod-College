from django.contrib import admin
from django import forms
from .models import Lecture, Schedules
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
class LectureAdmin(admin.ModelAdmin):
    list_display = ('facult',)
