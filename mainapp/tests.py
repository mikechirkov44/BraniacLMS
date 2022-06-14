from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus
from authapp.models import User
from mainapp.models import News

class StaticPagesSmokeTest(TestCase):
    
    def test_page_index_open(self):
        url = reverse('mainapp:main_page')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)
    
    def test_page_contacts_open(self):
        url = reverse('mainapp:contacts')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):
   
    def setUp(self) -> None:
        super().setUp()
        for i in range(5):
            News.objects.create(
                title='Test_news{i}',
                preamble='Preamble{i}',
                body='Body{i}'
            )
        User.objects.create_superuser(username='django_test', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login') 
        self.client_with_auth.post(
            auth_url,
            {'username':'django_test', 'password':'geekbrains'}
        )
    def test_open_page(self):
        url = reverse('mainapp:news')
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonym(self):
        url = reverse('mainapp:news_create')

        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_item_by_admin(self):

        news_count = News.objects.all().count()

        url = reverse('mainapp:news_create')
        result = self.client_with_auth.post(
            url,
            data={
                'title':'Test news',
                'preamble':'Test preamble',
                'body':'Test body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        self.assertEqual(News.objects.all().count(), news_count + 1)







    