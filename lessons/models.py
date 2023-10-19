from django.db import models
from datetime import date
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from users.models import User


class Lecture(models.Model):
    title = models.CharField('Название', max_length=150)
    description = models.CharField('Описание')
    lecturer = models.ForeignKey(User, verbose_name='Лектор', related_name='lectures', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Schedules(models.Model):
    facult = models.CharField('Название факультета', max_length=150)
    name2 = models.CharField('Пример: "3 курс ИСИП"', max_length=150, null=True, blank=True)
    date = models.CharField('Дата действия расписания', max_length=150)
    schedule = models.CharField('PDF ссылка на расписание', max_length=300)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'