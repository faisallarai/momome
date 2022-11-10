from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TransactionView

router = DefaultRouter()
router.register('', TransactionView, basename='')

urlpatterns = [
    path('', include(router.urls))
]
