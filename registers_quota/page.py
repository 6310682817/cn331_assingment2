from django.shortcuts import render
from django.db.models import Q
from .models import Subject, Student, Apply

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
        for subject in Subject.objects.filter(quota_status='Open'):
            if search_keyword.upper() in subject.sub_id.upper():
                search_subject.append(subject)
        return render(self.request, 'admin_view/search.html', {
            "subjects": search_subject,
            "search_keyword": search_keyword,
        })

    def checkStu(self):
        if self.request.method == "POST":
            subject = Subject.objects.get(pk=self.request.POST['subject'])
            list_students = subject.sub_apply.all() 
        return render(self.request, "admin_view/checkStu.html", {
            "students": Student.objects.all(),
            "subject": subject,
            "list_students" : list_students,
        })
    
    def checkSub(self):
        if self.request.method == "POST":
            student = Student.objects.get(pk=self.request.POST['student'])
            list_subjects = student.stu_apply.all()
        return render(self.request, "admin_view/checkSub.html", {
            "subject": Subject.objects.filter(quota_status='Open'),
            "student": student,
            "list_subjects": list_subjects,
        })
    
    def student(self):
        search_username = ""
        search_student = []
        if self.request.method == "POST":
            search_username = self.request.POST['search_username']
        for student in Student.objects.all():
            if search_username.upper() in student.stu_id or search_username.upper() in student.stu_name.upper():
                search_student.append(student)
        return render(self.request, "admin_view/student.html", {
            "students": search_student,
            "search_username": search_username,
        })

class StudentPage:
    def __init__(self, request):
        self.request = request
        self.user = Student.objects.get(pk=request.user)
        print(request.POST)
    
    def index(self):
        return render(self.request, 'reg/index.html', {  
            "student": self.user
        })

    def search(self):
        search_keyword = ''
        search_subject = []
        if self.request.POST.get('search_keyword'):
            search_keyword = self.request.POST['search_keyword']
        for subject in Subject.objects.filter(quota_status='Open'):
            if search_keyword.upper() in subject.sub_id:
                search_subject.append(subject)
        return render(self.request, 'reg/search.html', {
            "student": self.user,
            "subjects": search_subject,
            "search_keyword": search_keyword,
        })

    def status(self):
        applys = self.user.stu_apply.filter(Q(status='complete') | Q(status='withdraw'))
        return render(self.request, 'reg/status.html', {
            "student": self.user,
            "applys": applys,
        })
    
    def quota(self):
        search_keyword = ""
        search_subject = []
        applys = self.user.stu_apply.all()

        if self.request.POST.get('add'):
            subject = Subject.objects.get(pk=self.request.POST['add'])
            if not Apply.objects.filter(student=self.user, subject=subject):
                subject_add = Apply(student=self.user, subject=subject, status="add")
                subject_add.save()
        
        if self.request.POST.get('withdraw'):
            subject = Subject.objects.get(pk=self.request.POST['withdraw'])
            subject_withdraw = Apply.objects.get(student=self.user, subject=subject)
            subject_withdraw.status = "withdraw"
            subject_withdraw.save()

        if self.request.POST.get('cancel'):
            subject = Subject.objects.get(pk=self.request.POST['cancel'])
            subject_cancel = Apply.objects.get(student=self.user, subject=subject)
            if subject_cancel.status == "add":
                subject_cancel.delete()
            elif subject_cancel.status == "withdraw":
                subject_cancel.status = "complete"
                subject_cancel.save()
            
        if self.request.POST.get('search_keyword'):
            search_keyword = self.request.POST['search_keyword']
            for subject in Subject.objects.filter(quota_status='Open'):
                if search_keyword.upper() in subject.sub_id:
                    search_subject.append(subject)
        
        if self.request.POST.get('submit'):
            check_submit = True
            for apply in Apply.objects.filter(student=self.user):
                if apply.status == 'add':
                    tmp_subject = apply.subject
                    if tmp_subject.status == "N":
                        apply.delete()

                        check_submit = False

            if check_submit:
                search_keyword = ""
                for apply in Apply.objects.filter(student=self.user):
                    if apply.status == 'add':
                        tmp_subject = apply.subject
                        tmp_subject.seat += 1
                        if tmp_subject.seat == tmp_subject.max_seat:
                            tmp_subject.status = "N"
                        tmp_subject.save()

                        apply.status = "complete"
                        apply.save()
                    elif apply.status == 'withdraw':
                        tmp_subject = apply.subject
                        tmp_subject.seat -= 1
                        tmp_subject.status = "Y"
                        tmp_subject.save()
                        apply.delete()
                return self.status()

        add_apply = Apply.objects.filter(student=self.user, status='add')
        withdraw_apply = Apply.objects.filter(student=self.user, status='withdraw')
        complete_apply = Apply.objects.filter(student=self.user, status='complete')

        add_list = [subject.subject_id for subject in add_apply]
        withdraw_list = [subject.subject_id for subject in withdraw_apply]
        complete_list = [subject.subject_id for subject in complete_apply]

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