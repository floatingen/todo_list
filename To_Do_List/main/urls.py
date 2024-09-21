from django.urls import path, include
from rest_framework import routers

from .views import TaskViewSet, CategoryViewSet, PriorityViewSet

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('categories', CategoryViewSet)
router.register('priorities', PriorityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]