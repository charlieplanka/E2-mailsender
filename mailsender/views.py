from django.views.generic.list import ListView

from .models import Mail

LAST_QTY = 10


class MailListView(ListView):
    model = Mail
    context_object_name = 'last_mails'

    def get_queryset(self):
        qs = super().get_queryset()
        qs_last = qs.order_by('-id')[:LAST_QTY]
        return qs_last

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['last_qty'] = LAST_QTY
        return context
