import pytz
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail

from mailings.models import Mailing, MailingAttempt


def send_mailings():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(status__in=['created', 'running'])

    for mailing in mailings:
        last_attempt = mailing.mailingattempt_set.order_by('-attempt_date').first()

        if last_attempt:
            if mailing.periodicity == 'daily':
                next_send_date = last_attempt.attempt_date + timedelta(days=1)
            elif mailing.periodicity == 'weekly':
                next_send_date = last_attempt.attempt_date + timedelta(days=7)
            elif mailing.periodicity == 'monthly':
                next_send_date = last_attempt.attempt_date + relativedelta(months=1)
        else:
            next_send_date = mailing.created_at

        if current_datetime >= next_send_date:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()]
            )
            MailingAttempt.objects.create(mailing=mailing)
            mailing.status = 'running'
            mailing.save()
