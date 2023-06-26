import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
import django
django.setup()

from mentorconnect.models import User, Topic, Mentor, Student, Feedback

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




# You have a list with n members.
# Each element in the list is a color, either white, red or black.
# Arrange the elements in the list so that all the first elements are white, then red, then lastly  black.

# def sort_colors(colors):
#     white_count = 0
#     black_count = 0
#     red_count = 0
#     for color in colors:
#         if color == 'white':
#             white_count += 1
#         elif color == 'black':
#             black_count += 1
#         elif color == 'red':
#             red_count += 1
#     print(white_count, black_count, red_count)
#     for i in range(white_count):
#         colors[i] = 'white'
#     for i in range(red_count):
#         colors[i] = 'red'
#     for i in range(black_count):
#         colors[i] = 'black'
#
#     return colors
#
#
# colors = ['black', 'red', 'black', 'white', 'red', 'red', 'black', 'white', 'white', 'red', 'black']
#
# print(sort_colors(colors))

# Ori solution
# def sort_colors(lst):
#     r = 0
#     b = 0
#     w = 0
#
#     for item in lst:
#         if item == 'r':
#             r += 1
#         elif item == 'w':
#             w += 1
#         else:
#             b += 1
#
#     for i in range(len(lst)):
#         if w > 0:
#             lst[i] = 'w'
#             w -= 1
#             continue
#         if r > 0:
#             lst[i] = 'r'
#             r -= 1
#             continue
#
#         lst[i] = 'b'
#
#     return lst
#
# lst = ['r', 'r', 'w', 'b', 'b', 'w']
# print(sort_colors(lst))


