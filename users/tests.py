from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser 

class TestSetUp(APITestCase):

    def setUp(self) -> None:
        self.register_url = reverse("users:create-user")
        self.login_url = reverse('users:login-user')

        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    

class TestViews(TestSetUp):

    user_reg_data = {
            'username': 'remon',
            'email': 'remon@gmail.com',
            'password': '123456'
        }
    
    user_login_data_wrong = {
            'email': 'abul@gmail.com',
            'password': '123456'
        }
    
    user_login_data = {
            'email': 'remon@gmail.com',
            'password': '123456'
        }

    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)

        self.assertEqual(res.status_code, 409)

    def test_user_can_register_correctly(self):
        
        res = self.client.post(
            self.register_url, 
            self.user_reg_data, 
            format='json')
        self.assertEqual(res.data['email'], self.user_reg_data['email'])
        self.assertEqual(res.data['username'], self.user_reg_data['username'])
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_with_unverified_email(self):
        res = self.client.post(
            self.login_url, 
            self.user_login_data_wrong, 
            format='json')
        self.assertEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        response = self.client.post(
            self.register_url, 
            self.user_reg_data, 
            format='json')
        response_data = response.data
        # print(response_data)
        email = response.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(
            self.login_url, 
            self.user_login_data, 
            format='json')
        self.assertEqual(res.status_code, 200)
