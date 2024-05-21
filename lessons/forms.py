from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Reviews, Lecture
from users.models import Facult, Course, Group


class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'my_comment', 'id': 'my_comment', 'placeholder': 'Написать комментарий...'}))
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'style': 'width: 120px;'}))

    class Meta:
        model = Reviews
        fields = ('text', 'file')


class LectureForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Название'}))
    facult = forms.ModelChoiceField(queryset=Facult.objects.exclude(name='учитель'), label='Специальность')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Курс')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Группа')
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Lecture
        fields = ['title', 'description', 'facult', 'course', 'group']
