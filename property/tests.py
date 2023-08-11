from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Property
import requests

class TestSetUp(APITestCase):

    def setUp(self) -> None:
        # self.register_url = reverse("users:create-user")
        self.property_url = "http://127.0.0.1:8000/api/v2/property"
        # self.login_url = reverse('users:login-user')

        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    

class TestViews(TestSetUp):
    
    def test_get_all_property(self):
        res = requests.get(self.property_url)

        self.assertEqual(res.status_code, 200)
        
