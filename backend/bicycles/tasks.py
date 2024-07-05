from celery import shared_task
from django.core.mail import send_mail

from backend.constants import constants
from bicycles.models import Rent


@shared_task()
def task_execute(job_params):
    rent_value = (
        int(job_params.get('rent_duration')) * constants.TAX_PER_MINUTE
    )
    rent = Rent.objects.get(pk=job_params["rent_id"])
    rent.value = rent_value
    rent.save()
    send_mail(
        subject=constants.EMAIL_SUBJECT.format(id=rent.id),
        message=constants.EMAIL_TEXT.format(
            id=rent.id,
            name=rent.renter.username,
            bike=rent.bicycle.number,
            start=rent.start_time,
            finish=rent.finish_time,
            rent_duration=job_params.get('rent_duration'),
            value=rent_value
        ),
        from_email=constants.ADMIN_EMAIL,
        recipient_list=[rent.renter.email],
        fail_silently=False,
    )
