from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone

import threading
import logging
import datetime

logger = logging.getLogger(__name__)


class Mail(models.Model):
    address = models.EmailField(max_length=200)
    text = models.TextField()
    timeout = models.IntegerField(default=0)
    dispatch_time = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address}, created = {self.created_time.strftime("%m/%d/%Y %H:%M:%S")}, sent = {self.sent}'

    def save(self, **kwargs):
        self.dispatch_time = timezone.now() + datetime.timedelta(seconds=self.timeout)
        super().save(**kwargs)


@receiver(post_save, sender=Mail)
def add_mail_thread(instance, **kwargs):
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
        logger.info(f'Письмо успешно отправлено адресату: {mail.address}')
        change_mail_status(mail)
    except Exception as e:
        logging.error(f'При отправке письма произошла ошибка: {e}')


def change_mail_status(mail):
    Mail.objects.filter(pk=mail.pk).update(sent=True)
