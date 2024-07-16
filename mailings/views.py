from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.models import Mailing


class HomeView(ListView):
    model = Mailing
    template_name = 'mailings/home.html'


class MailingListView(ListView):
    model = Mailing
    paginate_by = 5

    def get_queryset(self):
        return Mailing.objects.all().order_by('-created_at')


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['clients', 'message', 'periodicity', 'status']
    success_url = reverse_lazy('mailings:mailing_detail')
    template_name = 'mailings/mailing_form.html'

    def form_valid(self, form):
        mailing = form.save()
        return redirect('mailings:mailing_detail', mailing.pk)


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['clients', 'message', 'periodicity', 'status']
    template_name = 'mailings/mailing_form.html'

    def get_success_url(self):
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')
