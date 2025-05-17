from django.contrib import admin
from .models import Student, StudentProfile, Semester

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'study_goal', 'personality_type')
    search_fields = ('user__username', 'user__email', 'study_goal', 'personality_type')

    def get_username(self, obj):
        return obj.user.username if obj.user else "No User Assigned"
    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email if obj.user else "No Email"
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "email")

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("student", "semester_number", "subjects")

admin.site.register(StudentProfile, StudentProfileAdmin)