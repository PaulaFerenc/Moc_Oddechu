from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from .models import Teacher, Workout, Client, Presence, Membership, WEEKDAYS


class AddTeacherForm(forms.Form):
    name = forms.CharField(label="Imię", max_length=64)
    surname = forms.CharField(label="Nazwisko", max_length=64)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefon")


class AddWorkoutForm(forms.Form):
    name = forms.CharField(label="Rodzaj", max_length=64)
    day = forms.ChoiceField(label="Dzień", choices=WEEKDAYS)
    time = forms.TimeField(label="Godzina")
    date = forms.DateField(label="Data")
    teacher = forms.ModelChoiceField(label="Nauczyciel", queryset=Teacher.objects.all())


class DelTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(label="Nauczyciel", queryset=Teacher.objects.all())