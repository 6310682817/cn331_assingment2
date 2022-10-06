from django.test import TestCase

from registers_quota.views import student
from .models import Student, Subject, SubjectData, Apply
from django.contrib.auth.models import User

# Create your tests here.

class QuotaModelsTestCase(TestCase):

    def setUp(self):

        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="Soft Engineering")

        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)
        

    def test_seat_available(self):
        """ is_seat_available should be True """

        subject = Subject.objects.first()

        self.assertTrue(subject.is_seat_available())

    def test_seat_not_available(self):
        """ is_seat_available should be False """

        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student1 = Student.objects.create(student=user1)

        subject = Subject.objects.first()

        subject.stu_apply.add(student1)

        self.assertFalse(subject.is_seat_available())

    def test_no_duplicate_subject(self):
        """ check_no_duplicate should be True """

        data1 = SubjectData.objects.first()
        subject2 = Subject.objects.create(subject=data1, sem="2", year="2022", seat=0, max_seat=1)

        check_no_duplicate = True
        for subject1 in Subject.objects.all():
            for subject2 in Subject.objects.exclude(id=subject1.id):
                if subject1.subject == subject2.subject and subject1.sem == subject2.sem and subject1.year == subject2.year:
                    check_no_duplicate = False

        self.assertTrue(check_no_duplicate)





