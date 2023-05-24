from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class UserModel(models.Model):
    email = models.EmailField(max_length=50, null=False, blank=True, db_index=True)
    password = models.CharField(max_length=30, validators=[validate_password], null=False)
    #  TODO: Password validation to ensure complexity level for security. Possibly also validate emails

    def __str__(self):
        return self.email


class Mentor(models.Model):
    # Really would only relevant if used here
    # identity_number = models.CharField(null=False, max_length=9, db_index=True)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    age = models.IntegerField(null=False)
    address = models.CharField(null=False, max_length=128)
    about_me = models.CharField(null=False, max_length=256) # Space to write about experience, education etc...
    #  TODO: profile_pic = .... upload picture routine ....
    user = models.OneToOneField(UserModel, on_delete=models.RESTRICT, related_name='mentor', null=False)
    students = models.ManyToManyField('Student', related_name='mentors')
    courses = models.ManyToManyField('Course', related_name='mentors')

    class Meta:
        db_table = 'mentor'

    def __str__(self):
        # If we use TZ number
        # return f"ID: {self.pk} person: {self.first_name} {self.last_name} TZ: {self.identity_number}"

        # Otherwise:
        return f"ID: {self.pk} Mentor: {self.first_name} {self.last_name}"


class Student(models.Model):
    # Really would only relevant if used here
    # identity_number = models.CharField(null=False, max_length=9, db_index=True)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    age = models.IntegerField(null=False)
    address = models.CharField(null=False, max_length=128)
    about_me = models.CharField(null=False, max_length=64) # brief description, ex. `12th Grade @ x High School`
    #  TODO: profile_pic = .... upload picture routine ....
    user = models.OneToOneField(UserModel, on_delete=models.RESTRICT, related_name='student', null=False)
    mentors = models.ManyToManyField('Mentor', related_name='students')
    courses = models.ManyToManyField('Course', related_name='students')

    class Meta:
        db_table = 'student'

    def __str__(self):
        # If we use TZ number
        # return f"ID: {self.pk} person: {self.first_name} {self.last_name} TZ: {self.identity_number}"

        # Otherwise:
        return f"ID: {self.pk} Student: {self.first_name} {self.last_name}"


class CourseCategory(models.Model):
    course_category = models.CharField(null=False, max_length=50)


class Course(models.Model):
    course_title = models.CharField(null=False, max_length=50)
    course_desc = models.CharField(null=False, max_length=128)
    category = models.ForeignKey(CourseCategory, on_delete=models.RESTRICT, related_name='courses', null=False)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return f"ID: {self.pk} Course: {self.course_title} Description: {self.course_desc}"


class FeedBack(models.Model):
    fb_title = models.CharField(null=False, max_length=50)
    fb_content = models.CharField(null=False, max_length=128)
    fb_stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='feedback')
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE, related_name='feedback')
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='feedback')

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"ID: {self.pk} Feedback for {self.mentor}, {self.course}: {self.fb_title} - {self.fb_content}. " \
               f"From: {self.student}"


class Accounts(models.Model):
    pass


class TimeTable(models.Model):
    pass
