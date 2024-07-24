import smtplib
import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt


def process_mailing(mailing):
    try:
        server_response = send_mail(
            mailing.message.subject,
            mailing.message.body,
            EMAIL_HOST_USER,
            [client.email for client in mailing.clients.all()],
            fail_silently=False,
        )
        MailingAttempt.objects.create(
            mailing=mailing,
            server_response=server_response,
            status_attempt=bool(server_response)
        )
        return True

    except smtplib.SMTPException as e:
        MailingAttempt.objects.create(
            mailing=mailing,
            server_response=str(e),
            status_attempt=False
        )
        return False


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
            success = process_mailing(mailing)
            if success:
                mailing.status = 'completed'
            else:
                mailing.status = 'failed'
            mailing.save()
