import io

from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
import logging
from rest_framework.exceptions import APIException

from bicycles.models import Rent
from backend.constants import constants
from backend.settings import MINIO_CLIENT


@shared_task()
def task_execute(job_params):
    rent_value = (
        int(job_params.get('rent_duration')) * constants.TAX_PER_MINUTE
    )
    rent = Rent.objects.get(pk=job_params["rent_id"])
    rent.value = rent_value
    rent.save()
    job_params = dict(
        id=rent.id,
        name=rent.renter.username,
        bike=rent.bicycle.number,
        start=rent.start_time,
        finish=rent.finish_time,
        rent_duration=job_params.get('rent_duration'),
        value=rent_value,
        recipient=rent.renter.email,
    )
    try:
        with transaction.atomic():
            transaction.on_commit(
                lambda: email_minio_services.delay(job_params)
            )
    except Exception as e:
        raise APIException(str(e))


@shared_task()
def email_minio_services(job_params):
    send_mail(
        subject=constants.EMAIL_SUBJECT.format(id=job_params.get('id')),
        message=constants.EMAIL_TEXT.format(
            id=job_params.get('id'),
            name=job_params.get('name'),
            bike=job_params.get('bike'),
            start=job_params.get('start'),
            finish=job_params.get('finish'),
            rent_duration=job_params.get('rent_duration'),
            value=job_params.get('value')
        ),
        from_email=constants.ADMIN_EMAIL,
        recipient_list=[job_params.get('recipient')],
        fail_silently=False,
    )
    rent_data = (f'Rent no.: {job_params.get("id")}\n'
                 f'User: {job_params.get("name")}\n'
                 f'Start time: {job_params.get("start")}\n'
                 f'Finish time: {job_params.get("finish")}')
    try:
        stream = io.BytesIO(bytes(rent_data, 'utf-8'))
        if not MINIO_CLIENT.bucket_exists(constants.MINIO_BUCKET_NAME):
            MINIO_CLIENT.make_bucket(constants.MINIO_BUCKET_NAME)
        file_name = (f'Rent-{job_params.get("id")}-('
                     f'{datetime.now().strftime("%d-%m-%Y")}).log')
        MINIO_CLIENT.put_object(bucket_name=constants.MINIO_BUCKET_NAME,
                                object_name=file_name, data=stream,
                                length=len(rent_data),
                                content_type='text/plain')
    except Exception as error:
        return logging.error(f'MinIO service is unavailable\n{error}')
