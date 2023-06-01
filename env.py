import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
import django
django.setup()

from mentorconnect.models import User, Topic, SubTopic, Mentor, Student, FeedBack

u = User(email='test4@gmail.com', password='123')
u.save()


# a = Mentor.objects.first().feedbacks.first()
# s = Student.objects.filter(first_name='אבי')[0]
# print(a)
# print(a.fb_content)

# print([(topic.sub_topic_name, topic.sub_topic_name) for topic in a.sub_topics.all()])