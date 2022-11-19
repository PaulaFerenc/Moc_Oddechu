from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from .models import Teacher, Workout, Client, Membership, WEEKDAYS, MEMBERSHIPS


class AddTeacherForm(forms.Form):
    name = forms.CharField(label="Imię", max_length=64)
    surname = forms.CharField(label="Nazwisko", max_length=64)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefon")


class DateInput(forms.DateInput):
    input_type = 'date'


class AddWorkoutForm(forms.Form):
    name = forms.CharField(label="Rodzaj", max_length=64)
    day = forms.ChoiceField(label="Dzień", choices=WEEKDAYS)
    time = forms.TimeField(label="Godzina")
    date = forms.DateField(widget=DateInput)
    teacher = forms.ModelChoiceField(label="Nauczyciel", queryset=Teacher.objects.all())


class DelTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(label="Nauczyciel", queryset=Teacher.objects.all())


class AddClientForm(forms.Form):
    name = forms.CharField(label="Imię", max_length=64)
    surname = forms.CharField(label="Nazwisko", max_length=64)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefon")


class EnrolClientForm(forms.Form):
    client = forms.ModelChoiceField(label="Klient", queryset=Client.objects.all())


class AddMembershipForm(forms.Form):
    type = forms.ChoiceField(label="Rodzaj", choices=MEMBERSHIPS)
    start = forms.DateField(widget=DateInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, max_length=50)


class EditClientForm(forms.Form):
    name = forms.CharField(label="Imię", max_length=64)
    surname = forms.CharField(label="Nazwisko", max_length=64)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefon")