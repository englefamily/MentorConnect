from django.contrib import admin
from .models import User, Mentor, Student, FeedBack, LearningTopic, LearningSubTopic
# Register your models here.

admin.site.register(User)
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(LearningTopic)
admin.site.register(LearningSubTopic)
admin.site.register(FeedBack)

