from django.db import models
from datetime import date
from django.urls import reverse
from django.utils import timezone
from datetime import datetime


class News(models.Model):
    title = models.CharField('Название', max_length=150)
    description = models.CharField('Описание')
    image = models.ImageField('Изображение')
    slug = models.SlugField(max_length=150, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


