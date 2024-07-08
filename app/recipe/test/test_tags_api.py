from django.contrib.auth import get_user_model

from django.urls import reverse

from django.test import TestCase

from rest_framework import status

from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    return reverse('recipe:tag-detail', args=[tag_id])


def create_user(email='usser@example.com', password='test1234'):

    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tst_auth_requiered(self):
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(
            user=self.user,
            name='Tag name'
        )
        Tag.objects.create(
            user=self.user,
            name='Tag test'
        )

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')

        serializer_data = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer_data.data)

    def test_tags_limited_to_user(self):
        new_user = get_user_model().objects.create_user(
            email='user10@example.com',
            password='1234556'
        )
        tag = Tag.objects.create(
            user=self.user,
            name='Tag name'
        )

        tag2 = Tag.objects.create(
            user=new_user,
            name='Tags test'
        )
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        tag = Tag.objects.create(
            user=self.user,
            name='Tag name test'
        )

        payload={'name': 'tag change'}

        url= detail_url(tag.id)

        res= self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):

        tag= Tag.objects.create(
            user=self.user,
            name='Tag sample'
        )
        url= detail_url(tag.id)
        res= self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Tag.objects.filter(user=self.user).exists())

