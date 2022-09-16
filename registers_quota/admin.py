from django.contrib import admin

from .models import Subject, Student, Apply
# Register your models here.


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("sub_id", "sub_name", "sem", "year", "seat", "max_seat", "status")

class StudentAdmin(admin.ModelAdmin):
    list_display = ("stu_id", "stu_name")

class ApplyAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "status")


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Apply, ApplyAdmin)
