from rest_framework import serializers


class ActiveSerializer(serializers.Serializer):
    active = serializers.FloatField()


class ReactiveSerilaizer(serializers.Serializer):
    reactive = serializers.FloatField()


class PowerSerializer(ActiveSerializer, ReactiveSerilaizer):
    pass
