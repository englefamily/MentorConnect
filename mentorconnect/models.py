from django.db import models
from django.contrib.auth.password_validation import validate_password

# Create your models here.

class UserModel(models.Model):
    email = models.EmailField(max_length=64, null=False, blank=True, db_index=True)
    password = models.CharField(max_length=64, validators=[validate_password], null=False)
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
    user = models.OneToOneField(UserModel, on_delete=models.RESTRICT, related_name='mentor', null=False)
    #  TODO: profile_pic = ....

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
    user = models.OneToOneField(UserModel, on_delete=models.RESTRICT, related_name='student', null=False)
    #  TODO: profile_pic = ....

    class Meta:
        db_table = 'student'

    def __str__(self):
        # If we use TZ number
        # return f"ID: {self.pk} person: {self.first_name} {self.last_name} TZ: {self.identity_number}"

        # Otherwise:
        return f"ID: {self.pk} Student: {self.first_name} {self.last_name}"