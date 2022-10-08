from xmlrpc.client import boolean
from django.test import TestCase, Client
from django.urls import reverse
from registers_quota.views import student
from .models import Student, Subject, SubjectData, Apply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class QuotaPageAdminTestCase(TestCase):
    def setUp(self):
        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")
        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student = Student.objects.create(student=user1)

        admin = User.objects.create_superuser(username="admin", password="1234")


    def test_search_subject(self):
        """ search_keyword and response context should be same """
        c = Client()
        c.login(username='admin', password='1234')
        response = c.post(reverse('admin_search'), data={'search_keyword': 'c'})

        self.assertEqual(response.context['search_keyword'], 'c')

    def test_search_student(self):
        """ search_keyword and response context should be same """
        c = Client()
        c.login(username='admin', password='1234')
        response = c.post(reverse('student'), data={'search_username': 'p'})

        self.assertEqual(response.context['search_username'], 'p')

class QuotaPageStudentTestCase(TestCase):
    def setUp(self):
        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")
        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student = Student.objects.create(student=user1)

        admin = User.objects.create_superuser(username="admin", password="1234")


    def test_search_subject(self):
        """ search_keyword and response context should be same """
        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('search'), data={'search_keyword': 'c'})

        self.assertEqual(response.context['search_keyword'], 'c')

    def test_add_subject_quota_page_student(self):
        """ response context count shound be 1 """

        subject = Subject.objects.first()

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'add': subject})

        self.assertEqual(response.context['add_apply'].count(), 1)

    def test_withdraw_subject_quota_page_student(self):
        """ response context count shound be 1 """

        subject = Subject.objects.first()

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'withdraw': subject})

        self.assertEqual(response.context['withdraw_apply'].count(), 1)

    def test_cancel_subject_quota_page_student(self):
        """ response context count shound be 1 """

        subject = Subject.objects.first()

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'add': subject})
        response = c.post(reverse('quota'), data={'cancel': subject})

        self.assertEqual(response.context['add_apply'].count(), 0)

    def test_search_subject_quota_page_student(self):
        """ search_keyword and response context should be same """

        subject = Subject.objects.first()

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'search_keyword': 'c'})

        self.assertEqual(response.context['search_keyword'], 'c')

    def test_full_seat_submit_quota_page_student(self):
        """ response context count shound be 0 """

        data = SubjectData.objects.first()
        subject = Subject.objects.create(subject=data, sem="2", year="2022", seat=0, max_seat=0)

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'add': subject})
        response = c.post(reverse('quota'), data={'submit': 'submit'})

        self.assertEqual(response.context['add_apply'].count(), 0)

    def test_add_submit_quota_page_student(self):
        """ response context count shound be 1 """

        data = SubjectData.objects.first()
        subject = Subject.objects.create(subject=data, sem="2", year="2022", seat=0, max_seat=1)

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'add': subject})
        response = c.post(reverse('quota'), data={'submit': 'submit'})
        self.assertEqual(response.context['applys'].count(), 1)

    def test_withdraw_submit_quota_page_student(self):
        """ response context count shound be 09 """

        data = SubjectData.objects.first()
        subject = Subject.objects.create(subject=data, sem="2", year="2022", seat=0, max_seat=1)

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.post(reverse('quota'), data={'withdraw': subject})
        response = c.post(reverse('quota'), data={'submit': 'submit'})
        self.assertEqual(response.context['applys'].count(), 0)

