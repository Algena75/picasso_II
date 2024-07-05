from datetime import datetime, timezone

from django.db import transaction
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from bicycles.models import Bicycle, Rent
from bicycles.serializers import (BicycleSerializer, FinishRentSerializer,
                                  RentSerializer)
from bicycles.tasks import task_execute


@extend_schema(tags=['Велосипеды'],
               summary='Список доступных велосипедов.')
@extend_schema_view(retrieve=extend_schema(exclude=True))
class BicycleViewSet(viewsets.ModelViewSet):
    queryset = Bicycle.objects.filter(is_rented=False)
    serializer_class = BicycleSerializer
    http_method_names = ('get', )


class RentView(APIView):
    serializer_class = RentSerializer

    @extend_schema(
        tags=['Аренда'], summary='Начать аренду'
    )
    def get(self, request, *args, **kwargs):
        bicycle = get_object_or_404(Bicycle, number=self.kwargs['bicycle_nr'])
        if bicycle.is_rented:
            return Response(
                {'detail': 'Велосипед уже арендован'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.rented:
            return Response(
                {'detail': 'Нельзя арендовать больше одного велосипеда'},
                status=status.HTTP_400_BAD_REQUEST
            )
        rent = Rent.objects.create(bicycle=bicycle, renter=request.user)
        bicycle.is_rented = True
        bicycle.save()
        request.user.rented = True
        request.user.save()
        data = model_to_dict(rent, fields=['id', 'bicycle', 'renter'])
        data.update(start_time=rent.start_time)
        serializer = RentSerializer(data=data)
        return Response(serializer.initial_data, status=status.HTTP_201_CREATED)


class FinishRentView(APIView):
    serializer_class = FinishRentSerializer

    @extend_schema(
        tags=['Аренда'], summary='Завершить аренду'
    )
    def get(self, request, *args, **kwargs):
        if not self.request.user.rented:
            return Response(
                {'detail': 'Вы не арендовали велосипед'},
                status=status.HTTP_400_BAD_REQUEST
            )
        rent = self.request.user.rents.filter(finish_time=None).first()
        if int(self.kwargs['bicycle_nr']) != rent.bicycle.number:
            return Response(
                {'detail': 'Этот велосипед не арендован Вами.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        rent.finish_time = datetime.now(timezone.utc)
        rent.save()
        self.request.user.rented = False
        self.request.user.save()
        rent.bicycle.is_rented = False
        rent.bicycle.save()
        rent_duration = rent.finish_time - rent.start_time
        rent_duration = rent_duration.total_seconds()
        if (rent_duration % 60) > 0:
            rent_duration = rent_duration // 60 + 1
        else:
            rent_duration = rent_duration // 60
        try:
            with transaction.atomic():
                job_params = dict(rent_id=rent.id,
                                  rent_duration=rent_duration)
                transaction.on_commit(lambda: task_execute.delay(job_params))
        except Exception as e:
            raise APIException(str(e))
        return Response(
            {'detail': f'Аренда завершена. Длительность - {rent_duration} м.'}
        )
