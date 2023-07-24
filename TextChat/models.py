from django.db import models
from mentorconnect import models as mc_models

# Create your models here.

class Chat(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    mentor = models.ForeignKey(mc_models.User, related_name='mentor_chats', on_delete=models.CASCADE, blank=True)
    student = models.ForeignKey(mc_models.User, related_name='student_chats', on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        if int(self.id.split('-')[0]) == int(self.id.split('-')[1]):
            raise ValueError("Mentor and Student cannot be the same User.")

        self.mentor_id = int(self.id.split('-')[0])
        self.student_id = int(self.id.split('-')[1])
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'chat'

    def __str__(self):
        return f'{self.id}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(mc_models.User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
