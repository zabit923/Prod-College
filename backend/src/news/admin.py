from django import forms
from django.contrib import admin

from .models import News
from ckeditor_uploader.widgets import CKEditorUploadingWidget




class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image')
    form = NewsAdminForm

