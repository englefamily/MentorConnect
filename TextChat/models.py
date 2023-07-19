from django.db import models
from mentorconnect import models as mc_models

# Create your models here.

class Chat(models.Model):
    id = models.CharField(max_length=13, primary_key=True)

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
