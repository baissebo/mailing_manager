from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingListView, HomeView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, ClientListView, \
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('mailing-list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create-mailing/', MailingCreateView.as_view(), name='mailing_create'),
    path('update-mailing/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete-mailing/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('client-list/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('create-client/', ClientCreateView.as_view(), name='client_create'),
    path('update-client-/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('delete-client/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message-list/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('create-message/', MessageCreateView.as_view(), name='message_create'),
    path('update-message/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('delete-message/<int:pk>/', MessageDeleteView.as_view(), name='message_delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
