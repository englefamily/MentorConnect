from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from .helphers import AGE_CHOICES, CITIES_CHOICES, EDUCATION_LEVEL, EDUCATION_COMPLETE, EDUCATION_START, EXPERIENCE_CHOICES, HOUR_CHOICES
from multiselectfield import MultiSelectField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id}, email: {self.email}'


class Mentor(models.Model):
    gender = models.CharField(null=False, choices=[('male', 'male'), ('female', 'female')], max_length=128)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    phone_num = models.CharField(null=False, unique=True, max_length=10)
    education_level = models.CharField(choices=EDUCATION_LEVEL, max_length=30, null=False)
    education_start = models.CharField(choices=EDUCATION_START, null=False, max_length=4)
    education_completion = models.CharField(choices=EDUCATION_COMPLETE, null=False, max_length=4)
    year_of_birth = models.CharField(choices=AGE_CHOICES, null=False, max_length=4)
    # TODO: Chananel - does Limud Naim etc have the full address of Mentors/ students?
    city_residence = models.CharField(choices=CITIES_CHOICES, max_length=128)
    study_cities = MultiSelectField(choices=CITIES_CHOICES, max_length=128, null=True, blank=True)
    self_description_title = models.CharField(null=False, max_length=256)
    self_description_content = models.CharField(null=False, max_length=700)
    # TODO: The following three fields are decimal - so that the Mentor can input a `rate` for that teaching methods
    teach_at_mentor = models.IntegerField(default=0)
    teach_at_student = models.IntegerField(default=0)
    teach_online = models.IntegerField(default=0)
    experience_with = MultiSelectField(choices=EXPERIENCE_CHOICES, max_length=30, null=True, blank=True)
    group_teaching = models.BooleanField(null=False, default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor', null=False)
    students = models.ManyToManyField('Student', related_name='mentors', blank=True)
    topics = models.ManyToManyField('Topic', related_name='mentors', blank=True)

    class Meta:
        db_table = 'mentor'

    def __str__(self):
        return f"ID: {self.pk} Mentor: {self.first_name} {self.last_name}"


class Student(models.Model):
    # TODO: error in students update and create in phone_number and email
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    phone_num = models.CharField(null=True, blank=True, unique=True, max_length=10)
    year_of_birth = models.CharField(null=True, blank=True,choices=AGE_CHOICES, max_length=4)
    # TODO: Josh added address_city & study_city to Student model
    address_city = models.CharField(null=True, blank=True,choices=CITIES_CHOICES, max_length=128)
    study_cities = MultiSelectField(null=True, blank=True,choices=CITIES_CHOICES, max_length=128)
    short_description = models.CharField(null=True, blank=True, max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', null=False)
    topics = models.ManyToManyField('Topic', related_name='students', blank=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        # If we use TZ number
        # return f"ID: {self.pk} person: {self.first_name} {self.last_name} TZ: {self.identity_number}"

        # Otherwise:
        return f"ID: {self.pk} Student: {self.first_name} {self.last_name}"


class Topic(models.Model):
    # TODO: Change to `null=False` for production
    name = models.CharField(null=True, max_length=50)
    field = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = 'topic'

    def __str__(self):
        return f"ID: {self.pk}, Topic name: {self.name} Topic field: {self.field}"


# class SubTopic(models.Model):
#     sub_topic_name = models.CharField(null=False, max_length=50)
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='courses', null=False)
#
#     class Meta:
#         db_table = 'sub_topic'
#
#     def __str__(self):
#         return f"ID: {self.pk}, Topic name: {self.topic.topic_name} Sub topic name: {self.sub_topic_name}"


class Feedback(models.Model):
    content = models.CharField(null=False, max_length=228)
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    # TODO: Josh tidied up these relationships - Since each `FeedBack` instance should be related to
    #  a single `SubTopic`, better to use `ForeignKey` not `ManyToManyField`
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='feedbacks')
    # Changed to ForeignKey
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='feedbacks', blank=True, null=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"ID: {self.pk} Feedback: {self.content} stars: {self.stars}"

    def clean(self):
        super().clean()
        if self.student not in self.mentor.students.all():
            raise ValidationError("Invalid feedback: The student is not associated with the mentor.")

class StudySessionSlot(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='study_session_slots')
    date = models.DateField()
    start_time = models.TimeField(choices=HOUR_CHOICES)
    end_time = models.TimeField(choices=HOUR_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='slots')
    teach_method = models.CharField(max_length=20, choices=TEACH_LOCATION_CHOICES)

    class Meta:
        db_table = 'study_session_slot'

    def __str__(self):
        return f"ID: {self.pk} Mentor: {self.mentor.first_name} {self.mentor.last_name} From: {self.start_time}, " \
               f"until: {self.end_time}"

    @property
    def rate(self):
        return getattr(self.mentor, f'teach_{self.teach_method}')


class StudySession(models.Model):
    slot = models.OneToOneField(StudySessionSlot, on_delete=models.CASCADE, related_name='study_session')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='study_sessions')
    session_happened = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'study_session'

    def __str__(self):
        return f"ID: {self.pk} Student: {self.student.first_name} {self.student.last_name} Session: {self.created_at}"


