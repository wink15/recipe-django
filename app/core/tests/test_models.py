"""Tests for models"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from core import models

class ModelTests(TestCase):

    def test_create_user_with_email_sucessfull(self):
        email='test@example.com'
        password='testpass123'
        user=get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalize(self):

        sample_emails=[
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['text4@example.COM', 'text4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample_123')
            print('a')
            print(user.email)
            self.assertEqual(user.email, expected)
    def test_new_user_without_email_raises_error(self):

        with self.assertRaises(ValueError):
             get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        user=get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):

        user= get_user_model().objects.create_user(
            'test@example.com',
            'test123',
        )

        recipe=models.Recipe.objects.create(
            user=user,
            title='test title',
            time_minute=5,
            price=Decimal('5.60'),
            descripcion= 'example description'
        )

        self.assertEqual(str(recipe), recipe.title )
