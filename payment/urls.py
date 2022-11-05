from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TransferView

router = DefaultRouter()
router.register('transfer', TransferView, basename='')

urlpatterns = [
    path('', include(router.urls))
]
