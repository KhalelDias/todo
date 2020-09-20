from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_execute(email, title, done_undone):
    send_mail('Task ', title+' was marked as '+done_undone,
              'diaskhalelov7@gmail.com', ['diaskhalelov7@gmail.com'],
              fail_silently=False)
    return None
