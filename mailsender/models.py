from django.db import models


class Mail(models.Model):
    address = models.EmailField(max_length=200)
    text = models.TextField()
    delay = models.IntegerField(default=0)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.adress}, sent = {self.sent}'