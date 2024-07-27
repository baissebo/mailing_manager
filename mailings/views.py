from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from forms import MailingForm, ClientForm
from mailings.models import Mailing, Client


class HomeView(ListView):
    model = Mailing
    template_name = 'home.html'


class MailingListView(ListView):
    model = Mailing
    paginate_by = 6

    def get_queryset(self):
        return Mailing.objects.all().order_by('-id')


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

    def form_valid(self, form):
        form.instance.status = 'created'
        self.object = form.save()
        return redirect('mailings:mailing_detail', pk=self.object.pk)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_success_url(self):
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')


class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Client.objects.all().order_by('-id')


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('mailings:client_detail')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'

    def get_success_url(self):
        return reverse('mailings:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')
    template_name = 'clients/client_confirm_delete.html'
