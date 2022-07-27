from django.db import models

WEEKDAYS = (
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
    (6, 'Sobota'),
    (7, 'Niedziela'),
)

MEMBERSHIPS = (
    (1, 'pojedyncze wejście'),
    (2, '4 wybór'),
    (3, '4 otwarty'),
    (4, '8 wybór'),
    (5, '8 otwarty'),
    (6, '12 wybór'),
    (7, '12 otwarty'),
    (8, 'open'),
)


class Teacher(models.Model):
    name = models.CharField(max_length=64, verbose_name='Imię')
    surname = models.CharField(max_length=64, verbose_name='Nazwisko')
    email = models.EmailField(max_length=254, verbose_name='Adres email')
    phone = models.CharField(max_length=32, verbose_name='Numer telefonu')

    def __str__(self):
        return f'{self.name} {self.surname}'


class Workout(models.Model):
    name = models.CharField(max_length=64, verbose_name='Rodzaj zajęć')
    day = models.IntegerField(choices=WEEKDAYS)
    time = models.TimeField(verbose_name='Godzina')
    date = models.DateField(verbose_name='Data')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Nauczyciel')

    def __str__(self):
        return f'{self.name} {self.day} {self.time} {self.date} {self.teacher}'


class Client(models.Model):
    name = models.CharField(max_length=64, verbose_name='Imię')
    surname = models.CharField(max_length=64, verbose_name='Nazwisko')
    email = models.EmailField(verbose_name='e-mail')
    phone = models.IntegerField()


class Presence(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Membership(models.Model):
    type = models.IntegerField(choices=MEMBERSHIPS, verbose_name='Rodzaj')
    start = models.DateTimeField(verbose_name='Ważny od')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
