# Generated by Django 4.2.5 on 2023-10-24 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_course_facult_user_facult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='course',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.course'),
        ),
        migrations.AlterField(
            model_name='user',
            name='facult',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.facult'),
        ),
    ]
