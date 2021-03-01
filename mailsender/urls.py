from django.urls import path

from .views import MailListView

urlpatterns = [
    path('', MailListView.as_view(), name='mail_list'),
]
