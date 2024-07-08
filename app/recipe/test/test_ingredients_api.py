from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL=reverse('recipe:ingredient-list')

def create_user(email='user@example.com', password='1234test'):

    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientsApiTest(TestCase):

    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        res=self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTest(TestCase):
    
    def setUp(self):
        self.client=APIClient()

        self.user=create_user()
        self.client.force_authenticate(self.user)
    
    def test_get_ingredients(self):

        Ingredient.objects.create(
            user=self.user,
            name='Ingrediente1'
        )
        Ingredient.objects.create(
            user=self.user,
            name='Ingrediente2'
        )

        res= self.client.get(INGREDIENTS_URL)

        ingredients= Ingredient.objects.all().order_by('-name')
        serializer= IngredientSerializer(ingredients, many=True)
        print(res.data)

        print(serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):

        ingredient1= Ingredient.objects.create(
            user=self.user,
            name='Ingr1'
        )
        user=create_user(email='user2@example.com', password='1234f')
        Ingredient.objects.create(
            user=user,
            name='Ingre2'
        )

        res= self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        self.assertEqual(res.data[0]['id'], ingredient1.id)

