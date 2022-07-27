from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Teacher, Workout, WEEKDAYS
from .forms import AddTeacherForm, AddWorkoutForm, DelTeacherForm


class HiView(View):
    def get(self, request, name):
        return HttpResponse(f'Hello {name}!')


class AddTeacherView(View):
    def get(self, request):
        form = AddTeacherForm()
        teachers = Teacher.objects.all()
        return render(request, 'add_teacher.html', {"form": form, "teachers": teachers})

    def post(self, request):
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            new_teacher = Teacher.objects.create(name=name, surname=surname, email=email,
                                                 phone=phone)
            return HttpResponse(f'Dodano nauczyciela {new_teacher}')
        else:
            return render(request, 'add_teacher.html', {"form": form})


class AddWorkoutView(View):
    def get(self, request):
        form = AddWorkoutForm()
        return render(request, 'add_workout.html', {"form": form})

    def post(self, request):
        form = AddWorkoutForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            day = form.cleaned_data['day']
            time = form.cleaned_data['time']
            date = form.cleaned_data['date']
            teacher = form.cleaned_data['teacher']
            new_workout = Workout.objects.create(name=name, day=day, time=time, date=date,
                                                 teacher=teacher)
            str_day = WEEKDAYS[int(day) - 1][1]
            return HttpResponse(
                f'Dodano trening: {new_workout.name}, {str_day}, {new_workout.time}, {new_workout.date}, {new_workout.teacher}')
        else:
            return render(request, 'add_workout.html', {"form": form})

class DelTeacherView(View):
    def get(self, request):
        form = DelTeacherForm()
        return render(request, 'del_teacher.html', {"form": form})

    def post(self, request):
        form = DelTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            teacher_id = teacher.pk
            Teacher.objects.get(pk=teacher_id).delete()

            return HttpResponse(f'Usunięto nauczyciela {teacher}')
        else:
            return render(request, 'del_teacher.html', {"form": form})


