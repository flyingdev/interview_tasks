from django.http import JsonResponse
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.

from .serializers import ActiveSerializer, ReactiveSerilaizer, PowerSerializer
from .services import run_simulation, set_values, get_active, get_reactive


class ApiView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def simulate(self, request):
        active_power, reactive_power = run_simulation()
        message = {'active': active_power, 'reactive': reactive_power}
        power = PowerSerializer(data=message)
        if power.is_valid():
            set_values(active_power, reactive_power)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(settings.NOTIFY_GROUP, {'type': 'notify', 'message': message})

            return JsonResponse(power.data)
        else:
            error = {'error_message': str(power.errors)}

            return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def active_power(self, request):
        value = get_active()

        message = {'active': value}
        active = ActiveSerializer(data=message)

        if active.is_valid():
            return JsonResponse(active.data)
        else:
            error = {'error_message': str(active.errors)}

            return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def reactive_power(self, request):
        value = get_reactive()

        message = {'reactive': value}
        reactive = ReactiveSerilaizer(data=message)

        if reactive.is_valid():
            return JsonResponse(reactive.data)
        else:
            error = {'error_message': str(reactive.errors)}

            return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
