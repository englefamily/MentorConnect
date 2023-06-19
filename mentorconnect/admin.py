from django.contrib import admin
from .models import User, Mentor, Student, Feedback, Topic
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Topic)
admin.site.register(Feedback)
