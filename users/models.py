from django.contrib.auth.models import AbstractUser
from django.db import models




class Facult(models.Model):
    name = models.CharField('Факультет', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'


class Course(models.Model):
    name = models.CharField('Курс', max_length=5)
    facult = models.ForeignKey(Facult, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} курс {self.facult}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class User(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    student_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150, null=True, blank=False)
    last_name = models.CharField(max_length=150, null=True, blank=False)
    username = models.CharField(unique=True, max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.first_name or self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TeacherLink(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    link = models.URLField()

    def __str__(self):
        return f"Ссылка для {self.course} от {self.teacher}"

    class Meta:
        verbose_name = 'Ссылка учителя'
        verbose_name_plural = 'Ссылки учителя'