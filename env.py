# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcproject.settings")
# import django
# django.setup()
#
# from mentorconnect.models import User, Topic, SubTopic, Mentor, Student, FeedBack
#
# u = User(email='test4@gmail.com', password='123')
# u.save()


# a = Mentor.objects.first().feedbacks.first()
# s = Student.objects.filter(first_name='אבי')[0]
# print(a)
# print(a.fb_content)

# print([(topic.sub_topic_name, topic.sub_topic_name) for topic in a.sub_topics.all()])

# create a function that takes a string and returns the most common character in the string
# def most_common_str():
#     string = input("input a string: ")
#     return max(set(string), key=string.count)
# print(most_common_str())



# def most_common_str():
#     charlist = []
#     string = input("input a string: ")
#     for char in string:
#         charlist.append(char)
#     return charlist
# print(most_common_str())


# Ori's example:
def get_most_common(word):
    assert len(word) > 0
    common_count = 0
    common_letter = None

    letters_dict = {}
    for letter in word:
        if letter not in letters_dict:
            letters_dict[letter] = 1
        else:
            letters_dict[letter] += 1

        if letters_dict[letter] > common_count:
            common_count = letters_dict[letter]
            common_letter = letter
    return common_letter
