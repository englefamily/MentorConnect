import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
import django
django.setup()

from mentorconnect.models import User, Topic, SubTopic, Mentor, Student, Feedback

# u = User.objects.all()[1]
# u.set_password('123')
# u.email = 'test2@gmail.com'
# u.save()
# print(User.objects.all()[1].password)

m = Mentor.objects.all()
for i in m:
    print(i.sub_topics.all())
# s = SubTopic.objects.get(sub_topic_name='Python')
# s.sub_topic_name = 'Python1'
# s.save()
# print(s)
# print(m)

