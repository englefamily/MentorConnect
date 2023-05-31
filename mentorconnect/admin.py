from django.contrib import admin
from .models import UserModel, Mentor, Student, CourseCategory, Course

# Register your models here.

admin.site.register(UserModel)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(CourseCategory)
admin.site.register(Course)
