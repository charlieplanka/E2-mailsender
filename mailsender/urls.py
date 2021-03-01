from django.urls import path

from .views import MailListView, SendMailView

urlpatterns = [
    path('', MailListView.as_view(), name='mail_list'),
    path('mails/create', SendMailView.as_view(), name='send_mail')
]
