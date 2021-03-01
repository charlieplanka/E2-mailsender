from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

import datetime
import threading
import logging

logger = logging.getLogger(__name__)


class Mail(models.Model):
    address = models.EmailField(max_length=200)
    text = models.TextField()
    timeout = models.IntegerField(default=0)
    dispatch_time = models.DateTimeField(blank=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address}, dispatch time = {self.dispatch_time.strftime("%m/%d/%Y, %H:%M:%S")}'

    def save(self, *args, **kwargs):
        self.dispatch_time = datetime.datetime.now() + datetime.timedelta(seconds=self.timeout)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Mail)
def add_mail_thread(instance, **kwargs):
    logging.info(instance.timeout)
    timeout = instance.timeout
    t = threading.Timer(timeout, send_new_mail, args=(instance,))
    t.start()


def send_new_mail(mail):
    try:
        send_mail(
            subject='Письмо от Skillfactory',
            message=mail.text,
            from_email=None,
            recipient_list=[mail.address],
            fail_silently=False,
        )
        logger.info('Письмо успешно отправлено')
        change_mail_status(mail)
    except Exception as e:
        logging.error(f'При отправке письма произошла ошибка: {e}')


def change_mail_status(mail):
    Mail.objects.filter(pk=mail.pk).update(sent=True)
