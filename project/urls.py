"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mo_app.views import AddTeacherView, AddWorkoutView, DelTeacherView, WorkoutsListView, WorkoutView, \
    DelWorkoutView, AddClientView, ClientsListView, EnrolClientView, ClientView, AddMembershipView, LoginView, \
    LogoutView, DelClientView, EditClientView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_teacher/', AddTeacherView.as_view()),
    path('add_workout/', AddWorkoutView.as_view()),
    path('del_teacher/', DelTeacherView.as_view()),
    path('', WorkoutsListView.as_view()),
    path('workout/<int:workout_id>/', WorkoutView.as_view()),
    path('del_workout/<int:workout_id>/', DelWorkoutView.as_view()),
    path('add_client/', AddClientView.as_view()),
    path('clients_list/', ClientsListView.as_view()),
    path('enrol_client/<int:workout_id>/', EnrolClientView.as_view()),
    path('client/<int:client_id>/', ClientView.as_view()),
    path('add_membership/<int:client_id>/', AddMembershipView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('del_client/<int:client_id>/', DelClientView.as_view()),
    path('edit_client/<int:client_id>/', EditClientView.as_view()),
]
