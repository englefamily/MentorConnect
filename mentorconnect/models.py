from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# class UserModel(models.Model):
#     # Ori says the get_user_model is better for the authentication etc that we will want to do
#     email = models.EmailField(max_length=50, null=False, blank=True, db_index=True)
#     password = models.CharField(max_length=30, validators=[validate_password], null=False)
#     #  TODO: Password validation to ensure complexity level for security. Possibly also validate emails
#
#     def __str__(self):
#         return self.email


# Creating CustomUser Models - Manager & object - after this is done `User` (variable) is used like other Django Models
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# Mentor model
class Mentor(models.Model):
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    mentor_hourly_rate = models.DecimalField(max_digits=3, decimal_places=2, null=False)
    #  TODO: Add About_me_title:
    #  TODO: Add About_me_content:
    #  TODO: Add DOB dropdown list:
    #  TODO: Add education_degree dropdown list:
    #  TODO: Add education_start dropdown list:
    #  TODO: Add education_end dropdown list:
    #  TODO: city with dropdown list CITY_CHOICES:
    #  TODO: profile_pic = .... upload picture routine ....
    #  TODO: Add other fields from Chananel's Models:
    #  TODO: link to `Payment` & `Report` classes?
    user = models.OneToOneField(CustomUser, on_delete=models.RESTRICT, related_name='mentor', null=False)
    students = models.ManyToManyField("Student", through="Course")

    def __str__(self):
        return f"Mentor: {self.last_name}, {self.first_name} {self.user.email}"

# class Mentor(models.Model):
#     # Really would only relevant if used here
#     # identity_number = models.CharField(null=False, max_length=9, db_index=True)
#     first_name = models.CharField(null=False, max_length=50)
#     last_name = models.CharField(null=False, max_length=50)
#     #  TODO: Change to DOB with dropdown list:
#     age = models.IntegerField(null=False)
#     #  TODO: Change to city with dropdown list CITY_CHOICES:
#     address = models.CharField(null=False, max_length=128)
#     about_me = models.CharField(null=False, max_length=256) # Space to write about experience, education etc...
#     #  TODO: profile_pic = .... upload picture routine ....
#     user = models.OneToOneField(UserModel, on_delete=models.RESTRICT, related_name='mentor', null=False)
#     students = models.ManyToManyField('Student', related_name='mentors')
#     courses = models.ManyToManyField('Course', related_name='mentors')
#     mentor_hourly_rate = models.DecimalField(max_digits=3, decimal_places=2, null=False)
#     #  TODO: link to `Payment` & `Report` classes?
#
#     class Meta:
#         db_table = 'mentor'
#
#     def __str__(self):
#         # If we use TZ number
#         # return f"ID: {self.pk} person: {self.first_name} {self.last_name} TZ: {self.identity_number}"
#
#         # Otherwise:
#         return f"ID: {self.pk} Mentor: {self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    #  TODO: Add About_me_title?
    #  TODO: Add About_me_content?
    #  TODO: Add DOB dropdown list:
    #  TODO: city with dropdown list CITY_CHOICES:
    #  TODO: profile_pic = .... upload picture routine ....
    #  TODO: Add other fields from Chananel's Models:
    #  TODO: link to `Payment` & `Report` classes?
    user = models.OneToOneField(CustomUser, on_delete=models.RESTRICT, related_name='student', null=False)

    def __str__(self):
        return f"Student: {self.last_name}, {self.first_name} {self.user.email}"

# class Student(models.Model):
#     # Really would only relevant if used here
#     # identity_number = models.CharField(null=False, max_length=9, db_index=True)
#     first_name = models.CharField(null=False, max_length=50)
#     last_name = models.CharField(null=False, max_length=50)
#     #  TODO: Change to DOB with dropdown list:
#     age = models.IntegerField(null=False)
#     #  TODO: Change to city with dropdown list CITY_CHOICES:
#     address = models.CharField(null=False, max_length=128)
#     about_me = models.CharField(null=False, max_length=64) # brief description, ex. `12th Grade @ x High School`
#     #  TODO: profile_pic = .... upload picture routine ....
#     user = models.OneToOneField(UserModel, on_delete=models.RESTRICT, related_name='student', null=False)
#     # Ori says we probably do Not need this as student is already connect to mentor by the Mentor's connection to Student
#     # we can check this in python shell by creating a student.mentor object
#     # mentors = models.ManyToManyField('Mentor', related_name='students')
#     # but he says we do need this as a student can have more than one course
#     courses = models.ManyToManyField('Course', related_name='students')
#
#     class Meta:
#         db_table = 'student'
#
#     def __str__(self):
#         # If we use TZ number
#         # return f"ID: {self.pk} person: {self.first_name} {self.last_name} TZ: {self.identity_number}"
#
#         # Otherwise:
#         return f"ID: {self.pk} Student: {self.first_name} {self.last_name}"


class CourseCategory(models.Model):
    course_category = models.CharField(null=False, max_length=50)

    class Meta:
        db_table = 'course_category'

    def __str__(self):
        return f"ID: {self.pk} Category {self.course_category}"


class Course(models.Model):
    course_title = models.CharField(null=False, max_length=50)
    course_desc = models.CharField(null=False, max_length=128)
    category = models.ForeignKey(CourseCategory, on_delete=models.RESTRICT, related_name='courses', null=False)
    mentor = models.ForeignKey(Mentor, on_delete=models.RESTRICT, null=False)
    students = models.ManyToManyField("Student", related_name="courses")

    class Meta:
        db_table = 'course'

    def __str__(self):
        return f"ID: {self.pk} Course: {self.course_title} by {self.mentor}"


# class FeedBack(models.Model):
#     fb_title = models.CharField(null=False, max_length=50)
#     fb_content = models.CharField(null=False, max_length=128)
#     fb_stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='feedback')
#     mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE, related_name='feedback')
#     course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='feedback')
#
#     class Meta:
#         db_table = 'feedback'
#
#     def __str__(self):
#         return f"ID: {self.pk} Feedback for {self.mentor}, {self.course}: {self.fb_title} - {self.fb_content}. " \
#                f"From: {self.student}"
#
#
# class Chat(models.Model):
#     mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='chats')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='chats')
#     message = models.CharField(max_length=256, null=False)
#     #  TODO: course_work = .... logic for send/ receive files ....
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db = 'chat'
#
#
# class TimeTable(models.Model):
#     MENTOR_AVAILABILITY = [
#         ('Available', 'Available'),
#         ('Not Available', 'Not Available'),
#     ]
#     mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='timetables')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
#     # Make a `booking` `intermediate table` to track which student booked the mentor's available block? See below...
#     start_time = models.DateTimeField(null=False)
#     end_time = models.DateTimeField(null=False)
#     availability = models.CharField(choices=MENTOR_AVAILABILITY, max_length=13, null=False)
#
#     class Meta:
#         db_table = 'timetable'
#
# # Todo: decide if needed.
# # `intermediate table` continued... Looks like good idea to me - but is it needed?
# # class Booking(models.Model):
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE)
# #     timetable = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
# #     booked_at = models.DateTimeField(auto_now_add=True)
# #
# # class Meta:
# #     db_table = 'booking'
#
#
# # This is just temporary. Just realising how difficult this will be to consider different banks worldwide.
# # Todo: Check with `Stripe` API to see what info is needed and if they provide the `model`s
# class Accounting(models.Model):
#     user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='accounting')
#     card_holder_name = models.CharField(max_length=50, null=False)
#     card_number = models.IntegerField(max_length=16, null=False)
#     cvc_number = models.IntegerField(max_length=3, null=False)
#
#     class Meta:
#         db_table = 'accounting'
#
#
# # This too is temporary.
# # Todo: Check with `Stripe` API...
# class Payment(models.Model):
#     PAYMENT_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Paid', 'Paid'),
#         ('Failed', 'Failed'),
#     ]
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
#     mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='payments')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
#     amount = models.DecimalField(max_digits=4, decimal_places=2, null=False)
#     status = models.CharField(choices=PAYMENT_CHOICES, max_length=20, null=False)
#
#     class Meta:
#         db_table = 'payment'
#
#
# # Todo: payment_due/ received should be linked to `Payment` class?
# class Report(models.Model):
#     mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='reports')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reports')
#     duration = models.DurationField(null=False)
#     payment_due = models.DecimalField(max_digits=4, decimal_places=2, null=False)
#     payment_received = models.DecimalField(max_digits=4, decimal_places=2, null=False)
#
#     class Meta:
#         db_table = 'report'
