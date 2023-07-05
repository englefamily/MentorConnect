import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
import django
django.setup()

from mentorconnect.models import User, Topic, Mentor, Student, Feedback

# m = Mentor.objects
# print(m.filter(study_cities__in=['jerusalem']))
from django.db.models import Q
#
# def get_mentors_by_cities(city_list):
#     conditions = Q()
#     for city in city_list:
#         conditions |= Q(study_cities__contains=city)
#     mentors = Mentor.objects.filter(conditions)
#     return mentors
#
# city_list = ['Haifa', 'Jerusalem']
# mentors = get_mentors_by_cities(city_list)
# print(mentors)


# m = Mentor.objects
# m=m.filter(topics__in=['5', '13']).distinct()
# m=m.filter(topics__in='6')
# print(m)
# for i in [8, 9]:
#     m.filter(topics__in=i)


from django.db.models import Count


# def get_mentors_by_topics(topic_list):
#     topic_set = set(topic_list)
#
#     mentors = Mentor.objects.filter(topics__id__in=topic_list) \
#         .annotate(match_count=Count('topics')) \
#         .order_by('-match_count')
#
#     return mentors
# topic_list = ['5', '6', '13']
# mentors = get_mentors_by_topics(topic_list)
# print(mentors)
mentors = Mentor.objects
mentors = mentors.filter(topics__id__in=[5,6]) \
        .annotate(match_count=Count('topics')) \
        .order_by('-match_count')

conditions = Q()
for city in ['Holon', 'Netanya']:
    conditions |= Q(study_cities__contains=city)
mentors = mentors.filter(conditions)
print(mentors)
