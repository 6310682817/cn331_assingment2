from django.db import models

# Create your models here.

class Subject(models.Model):
    sub_id = models.CharField(max_length=10, primary_key=True)
    sub_name = models.CharField(max_length=64)
    sem = models.IntegerField()
    year = models.IntegerField()
    seat = models.IntegerField()
    max_seat = models.IntegerField()
    status = models.CharField(max_length=10,choices=[('Open','Y'), ('Close','N')],default='Open')

    def __str__(self):
        return f"{self.sub_id} {self.sub_name}"

class Student(models.Model):
    stu_id = models.CharField(max_length=10, primary_key=True)
    stu_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.stu_id} {self.stu_name}"

class Apply(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="stu_apply")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sub_apply")
    status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.student} {self.subject}"

