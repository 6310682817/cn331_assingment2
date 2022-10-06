from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SubjectData(models.Model):
    sub_id = models.CharField(max_length=10, primary_key=True)
    sub_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sub_id}"

class Subject(models.Model):
    subject = models.ForeignKey(SubjectData, on_delete=models.CASCADE)
    sem = models.IntegerField()
    year = models.IntegerField()
    seat = models.IntegerField()
    max_seat = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('Open','Y'), ('Close','N')], default='Open')
    quota_status = models.BooleanField(default=True)

    class Meta:
        unique_together = ['subject', 'sem', 'year']

    def __str__(self):
        return f"{self.subject} {self.sem} {self.year}"

    def is_seat_available(self):
        return self.stu_apply.count() < self.max_seat

class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    applys = models.ManyToManyField(Subject, blank=True, related_name="stu_apply")

    def __str__(self):
        return f"{self.student.username} {self.student.first_name} {self.student.last_name}"

class Apply(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=[('empty','empty'), ('add','add'), 
                                                             ('withdraw','withdraw')], default='empty')

    def __str__(self):
        return f"{self.student} {self.subject} {self.status}"


