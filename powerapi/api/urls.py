from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ApiView


router = DefaultRouter()
router.register(r'power', ApiView, 'power')

urlpatterns = [
    path('v1/', include(router.urls))
]
