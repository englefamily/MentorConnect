from django.contrib import admin
from .models import User, Mentor, Student, FeedBack, Topic, SubTopic
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(FeedBack)
