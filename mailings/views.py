from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.forms import MailingForm, ClientForm, MessageForm
from mailings.models import Mailing, Client, Message


class HomeView(ListView):
    model = Mailing
    template_name = 'home.html'


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    paginate_by = 6

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not context['object_list']:
            context['no_mailings_message'] = True

        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = 'created'
        self.object = form.save()
        return redirect('mailings:mailing_detail', pk=self.object.pk)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_success_url(self):
        return reverse('mailings:mailing_detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user).order_by('-id')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'

    def get_success_url(self):
        return reverse_lazy('mailings:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return redirect('mailings:client_detail', pk=self.object.pk)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'

    def get_success_url(self):
        return reverse('mailings:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')
    template_name = 'clients/client_confirm_delete.html'


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/message_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user).order_by('-id')


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'messages/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'

    def get_success_url(self):
        return reverse('mailings:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        return redirect('mailings:message_detail', pk=self.object.pk)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/message_form.html'

    def get_success_url(self):
        return reverse('mailings:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')
    template_name = 'messages/message_confirm_delete.html'
