from django.shortcuts import render
from django.db.models import Q
from .models import Apply, Subject, SubjectData, Student
from django.contrib.auth.models import User

class AdminPage:
    def __init__(self, request):
        self.request = request
        self.adminUser = str(request.user)
    
    def index(self):
        return render(self.request, 'admin_view/index.html', {  
            "user": self.adminUser
        })

    def search(self):
        search_keyword = ''
        search_subject = []
        if self.request.POST.get('search_keyword'):
            search_keyword = self.request.POST['search_keyword']
        for subject in Subject.objects.filter(quota_status=True):
            if search_keyword.upper() in subject.subject.sub_id.upper():
                search_subject.append(subject)
        return render(self.request, 'admin_view/search.html', {
            "subjects": search_subject,
            "search_keyword": search_keyword,
        })

    def checkStu(self):
        if self.request.method == "POST":
            subject_data = SubjectData.objects.get(pk=self.request.POST['subject'].split()[0])
            subject = Subject.objects.get(subject=subject_data)
            list_students = subject.stu_apply.all() 
        return render(self.request, "admin_view/checkStu.html", {
            "students": Student.objects.all(),
            "subject": subject,
            "list_students" : list_students,
        })
    
    def checkSub(self):
        if self.request.method == "POST":
            user = User.objects.get(username=self.request.POST['student'])
            student = Student.objects.get(student=user)
            list_subjects = student.applys.all()
        return render(self.request, "admin_view/checkSub.html", {
            "subject": Subject.objects.filter(quota_status=True),
            "student": student,
            "list_subjects": list_subjects,
        })
    
    def student(self):
        search_username = ""
        search_student = []
        if self.request.method == "POST":
            search_username = self.request.POST['search_username']
        for student in Student.objects.all():
            if (search_username.upper() in student.student.username or
                search_username.upper() in student.student.first_name.upper() or
                search_username.upper() in student.student.last_name.upper()):
                search_student.append(student)
        return render(self.request, "admin_view/student.html", {
            "students": search_student,
            "search_username": search_username,
        })

class StudentPage:
    def __init__(self, request):
        self.request = request
        user = User.objects.get(username=request.user)
        self.user = Student.objects.get(student=user)
    
    def index(self):
        return render(self.request, 'reg/index.html', {  
            "student": self.user
        })

    def search(self):
        search_keyword = ''
        search_subject = []
        if self.request.POST.get('search_keyword'):
            search_keyword = self.request.POST['search_keyword']
        for subject in Subject.objects.filter(quota_status=True):
            if search_keyword.upper() in subject.subject.sub_id.upper():
                search_subject.append(subject)
        return render(self.request, 'reg/search.html', {
            "student": self.user,
            "subjects": search_subject,
            "search_keyword": search_keyword,
        })

    def status(self):
        applys = self.user.applys.all()
        return render(self.request, 'reg/status.html', {
            "student": self.user,
            "applys": applys,
        })
    
    def quota(self):
        search_keyword = ""
        search_subject = []
        applys = self.user.applys.all()

        if self.request.POST.get('add'):
            subject_data = SubjectData.objects.get(pk=self.request.POST['add'].split()[0])
            subject = Subject.objects.filter(subject=subject_data,
                                             sem=self.request.POST['add'].split()[1],
                                             year=self.request.POST['add'].split()[2]).first()
            Apply.objects.create(student=self.user, subject=subject, status="add")
        
        if self.request.POST.get('withdraw'):
            print(self.request.POST.get('withdraw'))
            subject_data = SubjectData.objects.get(pk=self.request.POST['withdraw'].split()[0])
            subject = Subject.objects.filter(subject=subject_data,
                                             sem=self.request.POST['withdraw'].split()[1],
                                             year=self.request.POST['withdraw'].split()[2]).first()
            Apply.objects.create(student=self.user, subject=subject, status="withdraw")

        if self.request.POST.get('cancel'):
            subject_data = SubjectData.objects.get(pk=self.request.POST['cancel'].split()[0])
            subject = Subject.objects.filter(subject=subject_data,
                                             sem=self.request.POST['cancel'].split()[1],
                                             year=self.request.POST['cancel'].split()[2]).first()
            Apply.objects.filter(student=self.user, subject=subject).delete()
            
        if self.request.POST.get('search_keyword'):
            search_keyword = self.request.POST['search_keyword']
            for subject in Subject.objects.filter(quota_status=True):
                if search_keyword.upper() in subject.subject.sub_id.upper():
                    search_subject.append(subject)
        
        if self.request.POST.get('submit'):
            check_submit = True
            for apply in Apply.objects.filter(student=self.user):
                if apply.status == 'add':
                    if not apply.subject.is_seat_available():
                        Apply.objects.filter(student=self.user, subject=apply.subject).delete()
                        check_submit = False

            if check_submit:
                search_keyword = ""
                for apply in Apply.objects.filter(student=self.user):
                    if apply.status == 'add':
                        self.user.applys.add(apply.subject)
                        apply.subject.seat = apply.subject.stu_apply.count()
                        apply.subject.save()
                        if not apply.subject.is_seat_available():
                            apply.subject.status = "N"
                            apply.subject.save()
                    elif apply.status == 'withdraw':
                        self.user.applys.remove(apply.subject)
                        apply.subject.status = "Y"
                        apply.subject.seat = apply.subject.stu_apply.count()
                        apply.subject.save()
                    apply.delete()
                return self.status()

        add_apply = Apply.objects.filter(student=self.user, status='add')
        withdraw_apply = Apply.objects.filter(student=self.user, status='withdraw')
        complete_apply = self.user.applys.all()
        add_list = [subject.subject.subject.sub_id for subject in add_apply]
        withdraw_list = [subject.subject.subject.sub_id for subject in withdraw_apply]
        complete_list = [subject.subject.sub_id for subject in complete_apply]

        return render(self.request, 'reg/quota.html', {
            "student": self.user,
            "subjects": search_subject,
            "search_keyword": search_keyword,
            "applys": applys,
            "complete_apply": complete_apply,
            "add_apply": add_apply,
            "withdraw_apply": withdraw_apply,
            "add_list": add_list,
            "withdraw_list": withdraw_list,
            "complete_list": complete_list,
        })