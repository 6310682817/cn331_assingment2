from django.contrib import admin

from .models import Apply, SubjectData, Subject, Student, Apply
# Register your models here.

class SubjectDataAdmin(admin.ModelAdmin):
    list_display = ("sub_id", "sub_name")

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject", "sem", "year", "seat", "max_seat", "status", "quota_status")

    @admin.action(description='Change status_enroll to true')
    def change_status_true(Subject, request, queryset):
        queryset.update(quota_status=True)

    @admin.action(description='Change status_enroll to false')
    def change_status_false(Subject, request, queryset):
        queryset.update(quota_status=False)

class StudentAdmin(admin.ModelAdmin):
    list_display = ("student",)
    filter_horizontal = ("applys",)

class ApplyAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "status")

admin.site.register(SubjectData, SubjectDataAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Apply, ApplyAdmin)

