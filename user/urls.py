from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user.views import CustomUserView

router = DefaultRouter()
router.register('', CustomUserView, basename='')

urlpatterns = [
    path('', include(router.urls))
]


