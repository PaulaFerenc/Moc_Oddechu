# Generated by Django 4.0.6 on 2022-07-26 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mo_app', '0003_teacher_surname'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='date',
            field=models.DateField(verbose_name='Data'),
            preserve_default=False,
        ),
    ]
