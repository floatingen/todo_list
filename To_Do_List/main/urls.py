from django.urls import path, include, re_path
from django.views.i18n import set_language, JavaScriptCatalog
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import (TaskViewSet, CategoryViewSet, PriorityViewSet, UserViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tasks', TaskViewSet)
router.register('categories', CategoryViewSet)
router.register('priorities', PriorityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'', include('login.urls')),
    re_path(r'', include('logout.urls')),
    re_path(r'i18n/setlang/', set_language, name='set_language'),
    re_path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
