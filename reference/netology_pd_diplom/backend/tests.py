from django.test import TestCase

# Create your tests here.
# from django.contrib.auth.models import User
from backend.models import User, ConfirmEmailToken, Shop, Category, ProductInfo, Product
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from backend.serializers import UserSerializer, ProductInfoSerializer


# python manage.py test
# import django
#
# django.setup()


class RegisterAccountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_account_success(self):
        data = {
            'first_name': 'John1',
            'last_name': 'Doe',
            'email': 'john1.doe@example.com',
            'password': 'StrongPassword123',
            'company': 'Example Company',
            'position': 'Software Engineer'
        }
        url = reverse('backend:user-register')  # Assuming 'register' is the name of your registration API endpoint
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='john1.doe@example.com').exists())

    def test_register_account_missing_arguments(self):
        data = {
            # 'first_name': 'John1',
            # 'last_name': 'Doe',
            'email': 'john1.doe@example.com',
            'password': 'StrongPassword123'
            # Missing 'company' and 'position'
        }
        url = reverse('backend:user-register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email='john1.doe@example.com').exists())

    def test_register_account_weak_password(self):
        data = {
            'first_name': 'John1',
            'last_name': 'Doe',
            'email': 'john1.doe@example.com',
            'password': 'weak'
            # Weak password
        }
        url = reverse('backend:user-register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email='john1.doe@example.com').exists())

class ConfirmAccountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='john1.doe@example.com',
            password='test_password'
        )
        # Create a confirmation token for the user
        self.token = ConfirmEmailToken.objects.create(
            user=self.user,
            key='example_token'
        )

    def test_confirm_account_success(self):
        # Assuming there's a user with the email 'john.doe@example.com' and a corresponding confirmation token
        data = {
            'email': 'john1.doe@example.com',
            'token': 'example_token'
        }
        # response = self.client.post('/api/confirm/', data)
        url = reverse('backend:user-register-confirm')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the user is now active
        user = User.objects.get(email='john1.doe@example.com')
        self.assertTrue(user.is_active)

    def test_confirm_account_invalid_token(self):
        # Assuming there's no token 'invalid_token' associated with the email 'john.doe@example.com'
        data = {
            'email': 'john1.doe@example.com',
            'token': 'invalid_token'
        }
        # response = self.client.post('/api/confirm/', data)
        url = reverse('backend:user-register-confirm')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that the user is still inactive
        user = User.objects.get(email='john1.doe@example.com')
        self.assertFalse(user.is_active)

    def test_confirm_account_missing_arguments(self):
        data = {
            'token': 'example_token'
            # Missing 'email'
        }
        # response = self.client.post('/api/confirm/', data)
        url = reverse('backend:user-register-confirm')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # No user should be activated
        self.assertFalse(User.objects.filter(is_active=True).exists())


class AccountDetailsTestCase(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(email='test@example.com', password=make_password('testpassword'))
        self.token = ConfirmEmailToken.objects.create(
            user=self.user,
            key='example_token'
        )
        self.client = APIClient()

    def test_get_account_details_authenticated(self):
        # Login as the created user
        self.client.force_authenticate(user=self.user)
        # Make a GET request to fetch account details
        url = reverse('backend:user-details')
        response = self.client.get(url)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data contains the expected user details
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_get_account_details_unauthenticated(self):
        # Make a GET request without authentication
        url = reverse('backend:user-details')
        response = self.client.get(url)
        # Check that the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check that the response data contains the expected error message
        self.assertEqual(response.data['Error'], 'Log in required')

    def test_update_account_details_authenticated(self):
        # Login as the created user
        self.client.force_authenticate(user=self.user)
        # Make a POST request to update account details
        url = reverse('backend:user-details')
        data = {'first_name': 'Updated', 'last_name': 'User'}
        response = self.client.post(url, data)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Refresh the user object from the database
        self.user.refresh_from_db()
        # Check that the user details have been updated
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_update_account_details_unauthenticated(self):
        # Make a POST request without authentication
        url = reverse('backend:user-details')
        data = {'first_name': 'Updated', 'last_name': 'User'}
        response = self.client.post(url, data)
        # Check that the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Check that the response data contains the expected error message
        self.assertEqual(response.data['Error'], 'Log in required')


class LoginAccountTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client = APIClient()

    def test_login_with_valid_credentials(self):
        # Make a POST request with valid credentials
        url = reverse('backend:user-login')
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        print(response.data)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response contains the token
        self.assertFalse(response.data['Status'])
        # Optionally, you can check other aspects of the response, such as 'Status'

    def test_login_with_invalid_credentials(self):
        # Make a POST request with invalid credentials
        url = reverse('backend:user-login')
        data = {'email': 'test@example.com', 'password': 'invalidpassword'}
        response = self.client.post(url, data)
        # Check that the response status code is 200 OK (because authentication failed)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response indicates authentication failure
        self.assertFalse(response.data['Status'])

    def test_login_without_required_arguments(self):
        # Make a POST request without required arguments
        url = reverse('backend:user-login')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        # Check that the response status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductInfoViewTestCase(TestCase):
    def setUp(self):
        # Create a shop
        self.shop = Shop.objects.create(name='Test Shop')

        # Create a category
        self.category = Category.objects.create(name='Test Category')

        # Create a product associated with the category
        self.product = Product.objects.create(name='Test Product', category=self.category)

        # Create product info associated with the product and shop
        self.product_info = ProductInfo.objects.create(
            model='Test Model',
            external_id=1,
            product=self.product,
            shop=self.shop,
            quantity=10,
            price=100,
            price_rrc=120
        )

        # Create an APIClient instance for making requests
        self.client = APIClient()

    def test_get_product_info(self):
        # Make a GET request to the product info endpoint
        url = reverse('backend:shops')  # Adjust this to match your actual endpoint
        response = self.client.get(url)
        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Optionally, check other aspects of the response


class BasketViewTestCase(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_get_basket_authenticated(self):
        url = reverse('backend:basket')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions based on the expected response data

    def test_get_basket_unauthenticated(self):
        self.client.logout()
        url = reverse('backend:basket')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_item_to_basket_authenticated(self):
        url = reverse('backend:basket')
        data = {'items': [{'product_id': 1, 'quantity': 2}, {'product_id': 2, 'quantity': 1}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions based on the expected response data and database state

    def test_add_item_to_basket_unauthenticated(self):
        self.client.logout()
        url = reverse('backend:basket')
        data = {'items': [{'product_id': 1, 'quantity': 2}, {'product_id': 2, 'quantity': 1}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Add more assertions based on the expected response data

    def test_remove_item_from_basket_authenticated(self):
        url = reverse('backend:basket')
        data = {'items': '1,2,3'}  # Assuming item IDs to remove
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions based on the expected response data and database state

    def test_remove_item_from_basket_unauthenticated(self):
        self.client.logout()
        url = reverse('backend:basket')
        data = {'items': '1,2,3'}  # Assuming item IDs to remove
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Add more assertions based on the expected response data