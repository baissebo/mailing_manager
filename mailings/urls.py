from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingListView, HomeView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('base/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create-mailing/', MailingCreateView.as_view(), name='mailing_create'),
    path('update-mailing/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete-mailing/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
