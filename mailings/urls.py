from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingListView, HomeView

app_name = MailingsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('base/', MailingListView.as_view(), name='mailing_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
