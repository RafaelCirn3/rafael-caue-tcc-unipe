from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_password_reset_email(email, reset_url):
    send_mail(
        subject='Redefinicao de senha - FinanceUp',
        message=f'Use o link para redefinir sua senha: {reset_url}',
        from_email='no-reply@financeup.local',
        recipient_list=[email],
        fail_silently=True,
    )
