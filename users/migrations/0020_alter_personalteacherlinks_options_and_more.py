# Generated by Django 4.2.5 on 2023-11-04 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_personalteacherlinks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personalteacherlinks',
            options={'verbose_name': 'Персональная ссылка', 'verbose_name_plural': 'Персональные ссылки'},
        ),
        migrations.AlterField(
            model_name='personalteacherlinks',
            name='link',
            field=models.CharField(),
        ),
    ]
