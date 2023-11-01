import uuid
from datetime import timedelta

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.utils.timezone import now

from .models import User, TeacherLink, Facult, Course, Group
from lessons.models import Lecture




class UserLoginForm(AuthenticationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    student_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'student_id', 'is_teacher')



class LinkForm(forms.ModelForm):
    facult = forms.ModelChoiceField(queryset=Facult.objects.exclude(name='учитель'), label='Специальность')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Курс')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Группа')
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), label='Ссылка')

    class Meta:
        model = TeacherLink
        fields = ('link', 'course', 'link')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    link_form = LinkForm()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image')



class LectureForm(forms.ModelForm):
    facult = forms.ModelChoiceField(queryset=Facult.objects.exclude(name='учитель'), label='Специальность')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Курс')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Группа')
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Lecture
        fields = ['title', 'description', 'facult', 'course', 'group']
