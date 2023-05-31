import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
import django
django.setup()

from mentorconnect.models import User, LearningTopic, LearningSubTopic, Mentor, Student, FeedBack

a = Mentor.objects.first()
print([(topic.sub_topic_name, topic.sub_topic_name) for topic in a.sub_topics.all()])