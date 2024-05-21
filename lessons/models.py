from django.db import models
from datetime import date
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from users.models import User, Course, Facult, Group




class Lecture(models.Model):
    title = models.CharField('Название', max_length=300)
    description = models.CharField('Описание')
    lecturer = models.ForeignKey(User, verbose_name='Лектор', related_name='lectures', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, default='')
    facult = models.ForeignKey(Facult, on_delete=models.SET_NULL, null=True, blank=True, default='')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True).order_by('-created_at')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Schedules(models.Model):
    facult = models.ForeignKey(Facult, on_delete=models.SET_NULL, null=True, blank=True, default='')
    date = models.CharField('Дата действия расписания', max_length=150)
    schedule = models.FileField('PDF ссылка на расписание', max_length=300)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class RPD(models.Model):
    facult = models.ForeignKey(Facult, on_delete=models.SET_NULL, null=True, blank=True, default='')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, default='')
    rpd = models.FileField('Файл с РПД', max_length=300)

    class Meta:
        verbose_name = 'РПД'
        verbose_name_plural = 'РПД'


class ProfDB(models.Model):
    facult = models.ForeignKey(Facult, on_delete=models.SET_NULL, null=True, blank=True, default='')
    link = models.URLField()

    class Meta:
        verbose_name = 'Проф. БД'
        verbose_name_plural = 'Проф. БД'


class Reviews(models.Model):
    name = models.ForeignKey(User, verbose_name='Имя', related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField('Коментарий')
    file = models.FileField('Файл', default='', null=True, blank=True, upload_to='review_files')
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.lecture}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
