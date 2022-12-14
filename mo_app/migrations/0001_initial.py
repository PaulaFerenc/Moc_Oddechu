# Generated by Django 4.0.6 on 2022-07-21 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Imię')),
                ('email', models.EmailField(max_length=254, verbose_name='Adres email')),
                ('phone', models.CharField(max_length=32, verbose_name='Numer telefonu')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Rodzaj zajęć')),
                ('day', models.IntegerField(choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek'), (6, 'Sobota'), (7, 'Niedziela')])),
                ('time', models.TimeField(verbose_name='Godzina')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mo_app.teacher', verbose_name='Nauczyciel')),
            ],
        ),
    ]
