from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (TaskViewSet, CategoryViewSet, PriorityViewSet, UserViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tasks', TaskViewSet)
router.register('categories', CategoryViewSet)
router.register('priorities', PriorityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
