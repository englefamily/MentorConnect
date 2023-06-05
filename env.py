import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
import django
django.setup()

from mentorconnect.models import User, Topic, SubTopic, Mentor, Student, FeedBack

u = User.objects.all()[1]
u.set_password('123')
u.email = 'test2@gmail.com'
u.save()
print(User.objects.all()[1].password)