from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Mail
from .forms import SendMailForm

import logging

LAST_QTY = 10
logger = logging.getLogger(__name__)


class MailListView(ListView):
    model = Mail
    context_object_name = 'last_mails'

    def get_queryset(self):
        qs = super().get_queryset()
        qs_last = qs.order_by('-created_time')[:LAST_QTY]
        return qs_last

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['last_qty'] = LAST_QTY
        return context


class SendMailView(CreateView):
    model = Mail
    form_class = SendMailForm
    success_url = reverse_lazy('mailsender:mail_list')
    template_name = 'send_mail.html'
