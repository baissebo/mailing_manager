from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.models import Mailing


class MailingListView(ListView):
    model = Mailing
    paginate_by = 10
    template_name = 'mailings/mailing_list.html'
    ordering = ['-created_at']

    def get_queryset(self):
        return Mailing.objects.all().order_by('created_at')


class MailingDetailView(DetailView):
    pass


class MailingCreateView(CreateView):
    pass


class MailingUpdateView(UpdateView):
    pass


class MailingDeleteView(DeleteView):
    pass
