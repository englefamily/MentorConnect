from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from .helphers import AGE_CHOICES, CITIES_CHOICES, EDUCATION_LEVEL, EDUCATION_COMPLETE, EDUCATION_START, TEACH_OPTIONS
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


class Mentor(models.Model):
    gender = models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=128)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    phone_num = models.CharField(null=False, unique=True, max_length=10)
    education = models.CharField(choices=EDUCATION_LEVEL, max_length=30)
    education_start_year = models.CharField(choices=EDUCATION_START, null=False, max_length=4)
    education_completion_year = models.CharField(choices=EDUCATION_COMPLETE, null=False, max_length=4)
    year_of_birth = models.CharField(choices=AGE_CHOICES, null=False, max_length=4)
    # TODO: Chananel - does Limud Naim etc have the full address of Mentors/ students?
    address_city = models.CharField(choices=CITIES_CHOICES, max_length=128)
    study_cities = MultiSelectField(choices=CITIES_CHOICES, max_length=128)
    short_description = models.CharField(null=False, max_length=256)
    long_description = models.CharField(null=False, max_length=700)
    cost_hour_min = models.PositiveIntegerField(validators=[MinValueValidator(50), MaxValueValidator(300)])
    cost_hour_max = models.PositiveIntegerField(validators=[MinValueValidator(50), MaxValueValidator(300)])
    teach_in = MultiSelectField(choices=TEACH_OPTIONS, max_length=30)
    experience_with = MultiSelectField(choices=[('adhd', 'adhd'), ('teaching', 'teaching')], max_length=30, null=True, blank=True)
    group_teaching = models.BooleanField(null=False, default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor', null=False)
    students = models.ManyToManyField('Student', related_name='mentors', blank=True)
    sub_topics = models.ManyToManyField('SubTopic', related_name='mentors')

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
    sub_topics = models.ManyToManyField('SubTopic', related_name='students', blank=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return f"ID: {self.pk} Student: {self.first_name} {self.last_name}"


class Topic(models.Model):
    topic_name = models.CharField(null=False, max_length=50)

    class Meta:
        db_table = 'topic'

    def __str__(self):
        return f"ID: {self.pk} topic name: {self.topic_name}"


class SubTopic(models.Model):
    sub_topic_name = models.CharField(null=False, max_length=50)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='courses', null=False)

    class Meta:
        db_table = 'sub_topic'

    def __str__(self):
        return f"ID: {self.pk}, Topic name: {self.topic.topic_name} Sub topic name: {self.sub_topic_name}"


class Feedback(models.Model):
    fb_content = models.CharField(null=False, max_length=228)
    fb_stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    # TODO: Josh tidied up these relationships - Since each `FeedBack` instance should be related to
    #  a single `SubTopic`, better to use `ForeignKey` not `ManyToManyField`
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='feedbacks')
    # Changed to ForeignKey
    sub_topic = models.ForeignKey('SubTopic', on_delete=models.CASCADE, related_name='feedbacks', blank=True, null=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"ID: {self.pk} Feedback: {self.fb_content} stars: {self.fb_stars}"

    def clean(self):
        super().clean()
        if self.student not in self.mentor.students.all():
            raise ValidationError("Invalid feedback: The student is not associated with the mentor 2.")
