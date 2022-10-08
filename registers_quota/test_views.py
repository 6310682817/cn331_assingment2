from xmlrpc.client import boolean
from django.test import TestCase, Client
from django.urls import reverse
from registers_quota.views import student
from .models import Student, Subject, SubjectData, Apply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class QuotaViewLoginPageTestCase(TestCase):
    def setUp(self):
        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")
        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student = Student.objects.create(student=user1)

        admin = User.objects.create_superuser(username="admin", password="1234")

    def test_login_view_status_code(self):
        """ login view's status code is ok """

        c = Client()
        response = c.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_login_page_status_code(self):
        """ login view's status code is ok """

        c = Client()
        response = c.post(reverse('login'), data={"username" : "6310682809", "password": "Reg1234."})
        self.assertEqual(response.status_code, 302)

    def test_can_not_login_view_status_code(self):
        """ login view's status code is ok """

        c = Client()
        response = c.post(reverse('login'), data={"username" : "6310682809", "password": "Reg1234"})
        self.assertEqual(len(response.context['message']), 20)

    def test_logout_view_status_code(self):
        """ login view's status code is ok """

        c = Client()
        response = c.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_not_login_index_page_status_code(self):
        """ index status code is 302 """

        c = Client()
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    # admin page
    def test_not_login_admin_search_page_status_code(self):
        """ admin_search status code is 302 """

        c = Client()
        response = c.get(reverse('admin_search'))
        self.assertEqual(response.status_code, 302)
    
    def test_not_login_admin_student_page_status_code(self):
        """ student status code is 302 """

        c = Client()
        response = c.get(reverse('student'))
        self.assertEqual(response.status_code, 302)

    def test_not_login_admin_checkStu_page_status_code(self):
        """ checkStu status code is 302 """

        c = Client()
        response = c.get(reverse('checkStu'))
        self.assertEqual(response.status_code, 302)

    def test_not_login_admin_checkSub_page_status_code(self):
        """ checkSub status code is 302 """

        c = Client()
        response = c.get(reverse('checkSub'))
        self.assertEqual(response.status_code, 302)

    # student page
    def test_not_login_student_search_page_status_code(self):
        """ search status code is 302 """

        c = Client()
        response = c.get(reverse('search'))
        self.assertEqual(response.status_code, 302)
    
    def test_not_login_student_quota_page_status_code(self):
        """ quota status code is 302 """

        c = Client()
        response = c.get(reverse('quota'))
        self.assertEqual(response.status_code, 302)

    def test_not_login_student_status_page_status_code(self):
        """ status status code is 302 """

        c = Client()
        response = c.get(reverse('status'))
        self.assertEqual(response.status_code, 302)

class QuotaViewAdminTestCase(TestCase):
    def setUp(self):
        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")
        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student = Student.objects.create(student=user1)

        admin = User.objects.create_superuser(username="admin", password="1234")
    
    def test_admin_login_pass(self):
        """ response should be True """

        c = Client()
        response = c.login(username='admin', password='1234')
        self.assertTrue(response)

    def test_admin_login_not_pass(self):
        """ response should be False """

        c = Client()
        response = c.login(username='admin', password='123')
        self.assertFalse(response)

    def test_admin_index_page_status_code(self):
        """ index status code is ok """

        c = Client()
        c.login(username='admin', password='1234')
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_admin_admin_search_page_status_code(self):
        """ admin_search status code is ok """

        c = Client()
        c.login(username='admin', password='1234')
        response = c.get(reverse('admin_search'))
        self.assertEqual(response.status_code, 200)

    def test_admin_search_page_student_login_status_code(self):
        """ admin_search status code is 302 """

        c = Client()
        c.login(username="6310682809", password="Reg1234.")
        response = c.get(reverse('admin_search'))
        self.assertEqual(response.status_code, 302)

    def test_admin_student_page_status_code(self):
        """ student status code is ok """

        c = Client()
        c.login(username='admin', password='1234')
        response = c.get(reverse('student'))
        self.assertEqual(response.status_code, 200)

    def test_admin_student_page_student_login_status_code(self):
        """ student_page status code is 302 """

        c = Client()
        c.login(username="6310682809", password="Reg1234.")
        response = c.get(reverse('student'))
        self.assertEqual(response.status_code, 302)
    
    def test_admin_checkStu_page_status_code(self):
        """ checkStu status code is ok """
        subject = Subject.objects.first()

        c = Client()
        c.login(username='admin', password='1234')
        response = c.post(reverse('checkStu'), data={"subject" : subject})
        self.assertEqual(response.status_code, 200)

    def test_admin_checkStu_page_student_login_status_code(self):
        """ checkStu_page status code is 302 """

        c = Client()
        c.login(username="6310682809", password="Reg1234.")
        response = c.get(reverse('checkStu'))
        self.assertEqual(response.status_code, 302)
    
    def test_admin_checkSub_page_status_code(self):
        """ checkSub status code is ok """
        student = Student.objects.first()

        c = Client()
        c.login(username='admin', password='1234')
        response = c.post(reverse('checkSub'), data={"student" : student.student})
        self.assertEqual(response.status_code, 200)

    def test_admin_checkSub_page_student_login_status_code(self):
        """ checkSub_page status code is 302 """

        c = Client()
        c.login(username="6310682809", password="Reg1234.")
        response = c.get(reverse('checkSub'))
        self.assertEqual(response.status_code, 302)

class QuotaViewStudentTestCase(TestCase):

    def setUp(self):
        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")
        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student = Student.objects.create(student=user1)

        admin = User.objects.create_superuser(username="admin", password="1234")

    def test_student_login_pass(self):
        """ response should be True """

        c = Client()
        response = c.login(username='6310682809', password='Reg1234.')
        self.assertTrue(response)

    def test_student_login_not_pass(self):
        """ response should be False """

        c = Client()
        response = c.login(username='6310682809', password='Reg1234')
        self.assertFalse(response)
    
    def test_student_index_page_status_code(self):
        """ index status code is ok """

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_student_search_page_status_code(self):
        """ search status code is ok """

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_student_search_page_admin_login_status_code(self):
        """ search status code is 302 """

        c = Client()
        c.login(username='admin', password='1234')
        response = c.get(reverse('search'))
        self.assertEqual(response.status_code, 302)

    def test_student_quota_page_status_code(self):
        """ quota status code is ok """

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.get(reverse('quota'))
        self.assertEqual(response.status_code, 200)

    def test_student_quota_page_admin_login_status_code(self):
        """ quota status code is 302 """

        c = Client()
        c.login(username='admin', password='1234')
        response = c.get(reverse('quota'))
        self.assertEqual(response.status_code, 302)

    def test_student_status_page_status_code(self):
        """ status status code is ok """

        c = Client()
        c.login(username='6310682809', password='Reg1234.')
        response = c.get(reverse('status'))
        self.assertEqual(response.status_code, 200)

    def test_student_status_page_admin_login_status_code(self):
        """ status_page status code is 302 """

        c = Client()
        c.login(username='admin', password='1234')
        response = c.get(reverse('status'))
        self.assertEqual(response.status_code, 302)

    
    

    