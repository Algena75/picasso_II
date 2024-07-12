import io
import sys

from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
import logging
from rest_framework.exceptions import APIException

from backend.constants import constants
from backend.settings import MINIO_CLIENT
from bicycles.models import Rent
if "pytest" not in sys.modules:
    from bicycles.spreadsheets import make_record


@shared_task()
def task_execute(job_params: dict):
    """
    Основная задача celery - рассчёт стоимости аренды. Здесь же происходит
    вызов функций отправки почтовых сообщений, сохранения log-файла в MinIO,
    добавления записи в google-таблицу. Надо поработать над 'чистотой')))
    """
    rent_value: int = (
        int(job_params.get('rent_duration')) * constants.TAX_PER_MINUTE
    )
    rent: Rent = Rent.objects.get(pk=job_params["rent_id"])
    rent.value = rent_value
    rent.save()
    job_params: dict = dict(
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
    try:
        from google.oauth2.service_account import Credentials  # noqa
        from googleapiclient import discovery  # noqa
        try:
            with transaction.atomic():
                transaction.on_commit(
                    lambda: make_google_record.delay(job_params)
                )
        except Exception as e:
            raise APIException(str(e))
    except Exception as error:
        return logging.error(f'Google Sheets are not installed\n{error}')


@shared_task()
def email_minio_services(job_params: dict):
    """
    Функция отправки почтового сообщения и сохранения log-файла в MinIO.
    Есть необходимость разделения функции на 2 для чистоты.
    """
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
    rent_data: str = (f'Rent no.: {job_params.get("id")}\n'
                      f'User: {job_params.get("name")}\n'
                      f'Start time: {job_params.get("start")}\n'
                      f'Finish time: {job_params.get("finish")}')
    try:
        stream = io.BytesIO(bytes(rent_data, 'utf-8'))
        if not MINIO_CLIENT.bucket_exists(constants.MINIO_BUCKET_NAME):
            MINIO_CLIENT.make_bucket(constants.MINIO_BUCKET_NAME)
        file_name: str = (f'Rent-{job_params.get("id")}-('
                          f'{datetime.now().strftime("%d-%m-%Y")}).log')
        MINIO_CLIENT.put_object(bucket_name=constants.MINIO_BUCKET_NAME,
                                object_name=file_name, data=stream,
                                length=len(rent_data),
                                content_type='text/plain')
    except Exception as error:
        return logging.error(f'MinIO service is unavailable\n{error}')


@shared_task()
def make_google_record(job_params: dict):
    """Подготовка значений и вызов функции добавления записи в google sheet"""
    list_values: list = [
        job_params.get('id'),
        job_params.get('name'),
        job_params.get('bike'),
        job_params.get('start').strftime("%d-%m-%Y %H:%M"),
        job_params.get('finish').strftime("%d-%m-%Y %H:%M"),
        job_params.get('rent_duration'),
        constants.TAX_PER_MINUTE,
        job_params.get('value')
    ]
    make_record(list_values)
