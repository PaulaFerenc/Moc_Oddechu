from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
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
            # str_day = WEEKDAYS[int(day) - 1][1]
            # return HttpResponse(
            #     f'Dodano trening: {new_workout.name}, {new_workout.day}, {new_workout.time}, {new_workout.date}, {new_workout.teacher}')
            return redirect(f'/')
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


class WorkoutsListView(View):
    def get(self, request):
        results = Workout.objects.all()
        return render(request, 'workouts_list.html', {'results': results})


class WorkoutView(View):
    def get(self, request, workout_id):
        workout = Workout.objects.get(id=workout_id)
        # workout = get_object_or_404(Workout, pk=workout_id)
        return render(request, 'workout.html', {'workout': workout})


class DelWorkoutView(View):
    def get(self, request, workout_id):
        del_workout = Workout.objects.get(id=workout_id)
        return render(request, 'del_workout.html', {"del_workout": del_workout})

    def post(self, request, workout_id):
        Workout.objects.get(id=workout_id).delete()
        return redirect(f'/')



class EnrolClientView(View):
    def get(self, request, workout_id):
