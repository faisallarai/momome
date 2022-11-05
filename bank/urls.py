from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BankView

router = DefaultRouter()
router.register('bank', BankView)

urlpatterns = [
    path('', include(router.urls))
]
