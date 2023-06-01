from django.contrib import admin
from .models import CustomUser, Mentor, Student, CourseCategory, Course

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(CourseCategory)
admin.site.register(Course)
