from rest_framework import serializers

from bicycles.models import Bicycle, Rent


class BicycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bicycle
        exclude = ('id', )


class RentSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(
        required=True,
        input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "iso-8601"]
    )
    finish_time = serializers.DateTimeField(
        required=True,
        input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "iso-8601"]
    )

    class Meta:
        model = Rent
        fields = ('bicycle', 'start_time', 'finish_time')


class FinishRentSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=256)
