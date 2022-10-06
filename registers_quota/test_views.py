from django.test import TestCase, Client
from django.urls import reverse
from registers_quota.views import student
from .models import Student, Subject, SubjectData, Apply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class QuotaViewTestCase(TestCase):

    def setUp(self):
        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")

        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")

    def test_login_view_status_code(self):
        """ login view's status code is ok """

        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_status_code(self):
        """ index view's status code is ok """

        c = Client()
        c.post(reverse('login'), {'username': "6310682809", 'password': "Reg1234."})
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    