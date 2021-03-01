from django.db import models
import datetime


class Mail(models.Model):
    address = models.EmailField(max_length=200)
    text = models.TextField()
    delay = models.IntegerField(default=0)
    dispatch_time = models.DateTimeField(blank=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address}, dispatch time = {self.dispatch_time.strftime("%m/%d/%Y, %H:%M:%S")}'

    def save(self, *args, **kwargs):
        self.dispatch_time = datetime.datetime.now() + datetime.timedelta(seconds=self.delay)
        super().save(*args, **kwargs)
