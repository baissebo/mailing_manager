import smtplib
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt


def process_mailing(mailing):
    try:
        mailing.status = 'running'
        mailing.save()

        server_response = send_mail(
            mailing.message.subject,
            mailing.message.body,
            EMAIL_HOST_USER,
            [client.email for client in mailing.clients.all()],
            fail_silently=False,
        )

        mailing.status = 'completed'
        mailing.save()
        MailingAttempt.objects.create(
            mailing=mailing,
            server_response=str(server_response),
            status_attempt=True
        )
        return True

    except smtplib.SMTPException as e:
        MailingAttempt.objects.create(
            mailing=mailing,
            server_response=str(e),
            status_attempt=False
        )
        return False


def get_next_send_date(mailing, last_attempt):
    if last_attempt:
        if mailing.periodicity == 'daily':
            return last_attempt.attempt_date + timedelta(days=1)
        elif mailing.periodicity == 'weekly':
            return last_attempt.attempt_date + timedelta(days=7)
        elif mailing.periodicity == 'monthly':
            return last_attempt.attempt_date + relativedelta(months=1)
    return mailing.created_at


def send_mailings():
    current_datetime = timezone.now()
    mailings = Mailing.objects.filter(status__in=['created', 'running'])

    for mailing in mailings:
        last_attempt = mailing.mailingattempt_set.order_by('-attempt_date').first()
        next_send_date = get_next_send_date(mailing, last_attempt)

        if current_datetime >= next_send_date:
            process_mailing(mailing)
