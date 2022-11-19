from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

from .models import Teacher, Workout, WEEKDAYS, Client, Presence, Membership
from .forms import AddTeacherForm, AddWorkoutForm, DelTeacherForm, AddClientForm, EnrolClientForm, AddMembershipForm, \
    LoginForm, EditClientForm


class AddTeacherView(LoginRequiredMixin, View):
    login_url = 'login'

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
            return redirect(f'/add_teacher/')
        else:
            return render(request, 'add_teacher.html', {"form": form})


class AddWorkoutView(LoginRequiredMixin, View):
    login_url = 'login'

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
            return redirect(f'/')
        else:
            return render(request, 'add_workout.html', {"form": form})


class DelTeacherView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = DelTeacherForm()
        return render(request, 'del_teacher.html', {"form": form})

    def post(self, request):
        form = DelTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            teacher_id = teacher.pk
            Teacher.objects.get(pk=teacher_id).delete()

            return redirect(f'/add_teacher/')
        else:
            return render(request, 'del_teacher.html', {"form": form})


class WorkoutsListView(LoginRequiredMixin, View):
    login_url = 'login'  # szuka po nazwie url'a (name=), a nie po danym url-u

    def get(self, request):
        # results = Workout.objects.all()
        results = Workout.objects.order_by('-date', '-time')
        return render(request, 'workouts_list.html', {'results': results})


class WorkoutView(LoginRequiredMixin, View):
    login_url = 'login'

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


class DelWorkoutView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, workout_id):
        del_workout = Workout.objects.get(id=workout_id)
        return render(request, 'del_workout.html', {'del_workout': del_workout})

    def post(self, request, workout_id):
        Workout.objects.get(id=workout_id).delete()
        return redirect(f'/')


class AddClientView(LoginRequiredMixin, View):
    login_url = 'login'

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


class ClientsListView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        results = Client.objects.all()
        return render(request, 'clients_list.html', {'results': results})


class EnrolClientView(LoginRequiredMixin, View):
    login_url = 'login'

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


class ClientView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        membership = Membership.objects.filter(client=client)
        validation = 'Brak karnetu'

        if membership:
            beg = membership.last().start
            end = beg + timedelta(days=30)
            if end >= timezone.now():
                validation = f'Aktywny karnet - ważny do  {end.date()}'
            else:
                validation = f'Karnet wygasł - ważny do: {end.date()}'
        return render(request, 'client.html', {'client': client, 'validation': validation})

        # start = membership.start.date()
        # start = request.GET.get['start']
        # start = datetime.strptime(start_str, "%Y-%m-%d")
        # end = start + timedelta(days=30)


class AddMembershipView(LoginRequiredMixin, View):
    login_url = 'login'

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


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(f'/')
            else:
                return HttpResponse('Nie udało się zalogować')
        else:
            return render(request, 'login.html', {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(f'/')


class DelClientView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, client_id):
        del_client = Client.objects.get(id=client_id)
        return render(request, 'del_client.html', {'del_client': del_client})

    def post(self, request, client_id):
        Client.objects.get(id=client_id).delete()
        return redirect(f'/clients_list/')


class EditClientView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, client_id):
        form = EditClientForm()
        client = Client.objects.get(id=client_id)
        return render(request, 'edit_client.html', {'form': form, 'client': client})

    # def post(self, request):
    #     form = EditClientForm(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data['name']
    #         surname = form.cleaned_data['surname']
    #         email = form.cleaned_data['email']
    #         phone = form.cleaned_data['phone']
    #         new_client = Client.objects.create(name=name, surname=surname, email=email,
    #                                            phone=phone)
    #         return redirect(f'/')
    #     else:
    #         return render(request, 'add_client.html', {"form": form})
