from django.test import TestCase
from django.test import Client

client = Client()
class mocOddechuTests(TestCase):

    def test_home_page(self):
        response = client.get('/')  # Pobieramy stronę metodą GET.
        return response.status_code == 200


# Create your tests here.
