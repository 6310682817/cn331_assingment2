from django.test import TestCase

from registers_quota.views import student
from .models import Student, Subject, SubjectData, Apply
from django.contrib.auth.models import User

# Create your tests here.

class QuotaModelsTestCase(TestCase):

    def setUp(self):

        data1 = SubjectData.objects.create(sub_id="CN331", sub_name="SOFTWARE ENGINEERING")
        subject1 = Subject.objects.create(subject=data1, sem="1", year="2022", seat=0, max_seat=1)

        data2 = SubjectData.objects.create(sub_id="CN340", sub_name="MACHINE LEARNING")
        subject2 = Subject.objects.create(subject=data2, sem="1", year="2022", seat=0, max_seat=1)

        data3 = SubjectData.objects.create(sub_id="CN320", sub_name="COMPUTER NETWORK CONFIGURATION")
        subject3 = Subject.objects.create(subject=data3, sem="1", year="2022", seat=0, max_seat=1, status = "Close")

        
        user1 = User.objects.create_user(username="6310682809", password="Reg1234.")
        student1 = Student.objects.create(student=user1)
        user2 = User.objects.create_user(username="6310682817", password="Reg1234.")
        student2 = Student.objects.create(student=user2)

    def test_seat_available(self):
        """ is_seat_available should be True """

        subject = Subject.objects.first()

        self.assertTrue(subject.is_seat_available())

    def test_seat_not_available(self):
        """ is_seat__not_available should be False """


        subject = Subject.objects.first()
        student = Student.objects.first()

        subject.stu_apply.add(student)

        self.assertFalse(subject.is_seat_available())

    def test_no_duplicate_subject(self):
        """ check_no_duplicate should be True """

        data1 = SubjectData.objects.first()
        subject1_2 = Subject.objects.create(subject=data1, sem="2", year="2022", seat=0, max_seat=1)

        check_no_duplicate = True
        for subject in Subject.objects.all():
            for subject1_2 in Subject.objects.exclude(id=subject.id):
                if subject.subject == subject1_2.subject and subject.sem == subject1_2.sem and subject.year == subject1_2.year:
                    check_no_duplicate = False

        self.assertTrue(check_no_duplicate)

    def test_student_no_duplicate_subject(self):
        """ check_student_no_duplicate_subject should be True """

        student = Student.objects.first()
        student.applys.add(Subject.objects.all()[0])
        student.applys.add(Subject.objects.all()[0])
        student.applys.add(Subject.objects.all()[1])

        check_student_no_duplicate_subject = True
        for subject in student.applys.all():
            for subject2 in Subject.objects.exclude(id=subject.id):
                if subject.subject == subject2.subject:
                    check_student_no_duplicate_subject = False

        self.assertTrue(check_student_no_duplicate_subject)
    
    def test_subject_no_duplicate_student(self):
        """ check_subject_no_duplicate_student should be True """

        student = Student.objects.first()
        subject = Subject.objects.first()

        subject.stu_apply.add(student)
        subject.stu_apply.add(student)
        check_subject_no_duplicate_student = True
        for student in subject.stu_apply.all():
            for student2 in Student.objects.exclude(id=student.id):
                if student.student.username == student2.student.username:
                    check_subject_no_duplicate_student = False

        self.assertTrue(check_subject_no_duplicate_student)

    def test_can_subject_status_Open(self):
        """ check_can_subject_status_Open should be True """

        student = Student.objects.first()
        subject = Subject.objects.first()

        student.applys.add(subject)

        check_can_subject_status_Open = False
        if student.applys.all().count() == 1:
            check_can_subject_status_Open = True

        self.assertTrue(check_can_subject_status_Open)

    def test_can_subject_status_Close(self):
        """ check_can_subject_status_Close should be False """

        student = Student.objects.first()
        subject = Subject.objects.all()[2]

        student.applys.add(subject)

        check_can_subject_status_Close = False
        if student.applys.all().count() == 1:
            check_can_subject_status_Close = True

        self.assertFalse(check_can_subject_status_Close)



