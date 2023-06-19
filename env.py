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

# m = Mentor.objects.all()
# for i in m:
#     print(i.sub_topics.all())
# s = SubTopic.objects.get(sub_topic_name='Python')
# s.sub_topic_name = 'Python1'
# s.save()
# print(s)
# print(m)

# students = Student.objects.all()
# print(len(students))
# for i in students:
#     print(i.mentors.all())
# print(students.sub_topics.all())

###############
# Mentor
# Sub_topic they teach
# Students in that sub_topic
# m = Mentor.objects.all()
# for i in m:
#     print(i)
#     for x in i.sub_topics.all():
#         print(' ',x)
#         print('     ',x.students.all())

# m = Mentor.objects.filter(sub_topics__sub_topic_name='Python')
# print(m)

# u = User.objects.get(email='teacher1@example.com')
# print(u.student.study_cities)
# print(u.mentor.sub_topics.all())

# fb = Feedback.objects.all()
# for i in fb:
#     print(i.student)
#     print(i.mentor)
#     print(i.sub_topic)
#     print(i.fb_content)
#     print(f"{i} \n")

# st = SubTopic.objects.all()
# for i in st:
#     print(i)
#     for x in i.mentors.all():
#         print(' ',x)
#         print('     ',i.feedbacks.all())


# create a function that rcv's two lists and checks if one list is identical in reversed order to the second list

# list0 = ['a','b','c','d','e','f']
# list1 = ['f','e','d','c','b','a']
# def check_if_reversed(list0, list1):
#     for i in range(len(list0)):
#         if list0[i] != list1[len(list1)-1-i]:
#             print('list do not match')
#         else:
#             print('list match')

# def check_if_reversed(list0, list1):
#     print(list0, list1)
#     print('list0')
#     for i in list0:
#         print(i)
#         for x in list1:
#             print(x)
#             if list0[i] == list1[-1-x]:
#                 continue
#             else:
#                 print('lists do not match')
#                 break


# print(type((1,)))
