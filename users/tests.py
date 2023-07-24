from django.test import TestCase, Client
from django.urls import reverse
from users.models import Product, Order, OrderItem
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = {'username': 'user.username','email':'user@gmail.com','first_name': 'user.first_name','last_name': 'user.last_name','password':'Ar@4120108'}
        self.login_details = {'username': self.user['username'], 'password': self.user['password']}
        # self.user_data = reverse('user')
        self.register_user = reverse('register')
        # self.register_product = reverse('register_product')
        # self.product = reverse('products')
        # self.gud = reverse('gud')

    def test_register_api(self):
        response = self.client.post(self.register_user, self.user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Success")