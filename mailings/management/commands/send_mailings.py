from django.core.management import BaseCommand

from cron import send_mailings


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mailings()
