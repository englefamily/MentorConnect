from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxValueValidator, MinValueValidator
from .helphers import AGE_CHOICES, CITIES_CHOICES
from django.contrib.auth.base_user import BaseUserManager


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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Mentor(models.Model):
    gender = models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=128)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    year_of_birth = models.CharField(choices=AGE_CHOICES, null=False, max_length=4)
    address_city = models.CharField(choices=CITIES_CHOICES, max_length=128)
    short_description = models.CharField(null=False, max_length=256)
    long_description = models.CharField(null=False, max_length=700)
    teach_online = models.BooleanField(null=False, default=False)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='mentor', null=False)
    students = models.ManyToManyField('Student', related_name='mentors', null=True, blank=True)
    sub_topics = models.ManyToManyField('LearningSubTopic', related_name='mentors')

    class Meta:
        db_table = 'mentor'

    def __str__(self):
        return f"ID: {self.pk} Mentor: {self.first_name} {self.last_name}"



class Student(models.Model):
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    year_of_birth = models.CharField(choices=AGE_CHOICES, null=False, max_length=4)
    address_city = models.CharField(choices=CITIES_CHOICES, max_length=128)
    short_description = models.CharField(null=False, max_length=256) # brief description, ex. `12th Grade @ x High School`
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='student', null=False)
    sub_topics = models.ManyToManyField('LearningSubTopic', related_name='students',  blank=True)
    # mentors = models.ManyToManyField('Mentor', related_name='students')

    class Meta:
        db_table = 'student'

    def __str__(self):
        return f"ID: {self.pk} Student: {self.first_name} {self.last_name}"


class LearningTopic(models.Model):
    topic_name = models.CharField(null=False, max_length=50)

    class Meta:
        db_table = 'topic'

    def __str__(self):
        return f"ID: {self.pk} Sub topic name: {self.topic_name}"


class LearningSubTopic(models.Model):
    sub_topic_name = models.CharField(null=False, max_length=50)
    topic = models.ForeignKey(LearningTopic, on_delete=models.RESTRICT, related_name='courses', null=False)

    class Meta:
        db_table = 'sub_topic'

    def __str__(self):
        return f"ID: {self.pk} Sub topic name: {self.sub_topic_name}"


class FeedBack(models.Model):
    fb_content = models.CharField(null=False, max_length=228)
    fb_stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='feedbacks')
    # sub_topic = models.CharField(max_length=100, choices=[], null=True, blank=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"ID: {self.pk} Feedback: {self.fb_content}"

    # def save(self, *args, **kwargs):
    #     mentor_sub_topics = self.mentor.sub_topics.all()
    #     self._meta.get_field('sub_topic').choices = [(topic.sub_topic_name, topic.sub_topic_name) for topic in mentor_sub_topics]
    #     super(FeedBack, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        mentor_sub_topics = self.mentor.sub_topics.all()
        self._meta.get_field('sub_topic').choices = [('a', 'a'), ('b', 'b')]
        super().__init__(*args, **kwargs)

