# Generated by Django 4.2.5 on 2023-11-12 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0022_alter_schedules_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Название'),
        ),
    ]
