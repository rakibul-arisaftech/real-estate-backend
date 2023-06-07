import os
import io

from PIL import Image

from django.urls import reverse, reverse_lazy, resolve
from django.conf import settings
from backend.settings import MEDIA_ROOT

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self) -> None:
        self.register_url = reverse("users:create-user")
        self.login_url = reverse('users:login-user')
        self.create_service_url = resolve('/api/v1/service/')

        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()


class TestViews(TestSetUp):

    def generate_photo_file():
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    user_reg_data = {
            'username': 'remon',
            'email': 'remon@gmail.com',
            'password': '123456'
        }
    
    user_login_data = {
            'email': 'remon@gmail.com',
            'password': '123456'
        }
    
    photo_file = generate_photo_file()

    data = {
            'title': 'a service test',
            'description': 'good service',
            'photo':photo_file
            }


    # /media/remon/Study/Office/real-estate-backend/backend/media/images/service/intern_law_B0o6u3G.jpg
    def test_user_can_create_service_after_verification(self):
        # os.path.join(settings.MEDIA_ROOT, "/media/images/service/")
        print(f"This is the current path: {os.getcwd()}")
        # with open(os.path.join(MEDIA_ROOT, '/images/service/intern_law_B0o6u3G.jpg'), 'rb') as photo_file:
        test_image = open("/media/remon/Study/Office/real-estate-backend/backend/media/images/service/intern_law_B0o6u3G.jpg", "rb")
        print(f"test_image {test_image}")
        data = {
            'title': 'a service test',
            'description': 'good service',
            # 'photo': test_image
            }
        # im = Image.open(photo_file)
        # im.show()
        response = self.client.post(
            self.register_url,
            self.user_reg_data,
            format='json')
        access_token = response.data['tokens']["access"]
        print(f"This is the token {access_token}")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        res = self.client.post(
            "/api/v1/service/",
            data,
            format="multipart"
        )
        print(f"This is res: {res.data}")
        self.assertEqual(res.status_code, 201)
