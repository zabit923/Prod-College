from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

from .models import User, TeacherLink, Facult, Course, Group, PersonalTeacherLinks


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
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Ваше сообщение'}),
                           label='Сообщение')

    class Meta:
        model = TeacherLink
        fields = ('link', 'course', 'link')


class PersonalLinkForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Название'}))
    facult = forms.ModelChoiceField(queryset=Facult.objects.exclude(name='учитель'), required=False, label='Специальность')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False, label='Курс')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Группа')
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Ссылка'}))
    private = forms.BooleanField(required=False, label='Только у меня')

    class Meta:
        model = PersonalTeacherLinks
        fields = ('title', 'link')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': 'readonly'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': 'readonly'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    link_form = LinkForm()
    personal_link_form = PersonalLinkForm()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image')
