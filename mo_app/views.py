from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from datetime import datetime
from datetime import timedelta
from django.utils import timezone


from .models import Teacher, Workout, WEEKDAYS, Client, Presence, Membership
from .forms import AddTeacherForm, AddWorkoutForm, DelTeacherForm, AddClientForm, EnrolClientForm, AddMembershipForm


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
        clients = Client.objects.filter(workout=workout_id)
        # workout = get_object_or_404(Workout, pk=workout_id)
        return render(request, 'workout.html', {'workout': workout, 'clients': clients})

    def post(self, request, workout_id):
        client = request.POST['id']
        cl = Client.objects.get(id=client)
        Presence.objects.get(workout=workout_id, client=cl).delete()
        # p = Presence.objects.get(workout=workout_id, client=cl)
        return redirect(f'/workout/{workout_id}')


class DelWorkoutView(View):
    def get(self, request, workout_id):
        del_workout = Workout.objects.get(id=workout_id)
        return render(request, 'del_workout.html', {'del_workout': del_workout})

    def post(self, request, workout_id):
        Workout.objects.get(id=workout_id).delete()
        return redirect(f'/')


class AddClientView(View):
    def get(self, request):
        form = AddClientForm()
        return render(request, 'add_client.html', {'form': form})

    def post(self, request):
        form = AddClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            new_client = Client.objects.create(name=name, surname=surname, email=email,
                                               phone=phone)
            # return HttpResponse(f'Dodano klienta {new_client}')
            return redirect(f'/')
        else:
            return render(request, 'add_client.html', {"form": form})


class ClientsListView(View):
    def get(self, request):
        results = Client.objects.all()
        return render(request, 'clients_list.html', {'results': results})


class EnrolClientView(View):
    def get(self, request, workout_id):
        form = EnrolClientForm()
        return render(request, 'enrol_client.html', {'form': form, 'workout': workout_id})

    def post(self, request, workout_id):
        form = EnrolClientForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            workout = Workout.objects.get(id=workout_id)
            if not Presence.objects.filter(workout=workout, client=client):
                Presence.objects.create(workout=workout, client=client)
                return redirect(f'/workout/{workout_id}/')
            else:
                return HttpResponse(f"Uczestnik już zapisany <a href='/'>OK</a>")
        else:
            return render(request, 'enrol_client.html', {"form": form})


class ClientView(View):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        membership = Membership.objects.filter(client=client)
        #
        # for result in membership:
        #     beg = result.start
        #     end = beg + timedelta(days=30)
        #     if end <= timezone.now():
        #         validation = result
        #     else:
        #         validation = f'Brak ważnych karnetów'
        return render(request, 'client.html', {'client': client, 'membership': membership})

        # start = membership.start.date()
        # start = request.GET.get['start']
        # start = datetime.strptime(start_str, "%Y-%m-%d")
        # end = start + timedelta(days=30)


class AddMembershipView(View):
    def get(self, request, client_id):
        form = AddMembershipForm()
        client = Client.objects.get(id=client_id)
        return render(request, 'add_membership.html', {'form': form, 'client': client})

    def post(self, request, client_id):
        form = AddMembershipForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            start = form.cleaned_data['start']
            client = Client.objects.get(id=client_id)
            Membership.objects.create(type=type, start=start, client=client)
            return redirect(f'/client/{client_id}/')
        else:
            return render(request, 'add_membership.html', {"form": form})
