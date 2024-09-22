from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import TaskSerializer, CategorySerializer, PrioritySerializer, UserSerializer
from .models import Task, Category, Priority
from django.utils import timezone


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path=r'status/(?P<status>\w+)')
    def get_tasks_by_status(self, request, status=None):
        tasks_by_status = {
            True: Task.objects.filter(status=status),
            False: Task.objects.filter(status=status, deleted=False, created_by=request.user.username)
        }[request.user.is_staff]

        serializer = TaskSerializer(tasks_by_status, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path=r'category/(?P<category>\d+)')
    def get_tasks_by_category(self, request, category=None):
        tasks_by_category = {
            True: Task.objects.filter(category=category),
            False: Task.objects.filter(category=category, deleted=False, created_by=request.user.username)
        }[request.user.is_staff]

        serializer = TaskSerializer(tasks_by_category, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path=r'priority/(?P<priority>\d+)')
    def get_tasks_by_priority(self, request, priority=None):
        tasks_by_priority = {
            True: Task.objects.filter(priority=priority),
            False: Task.objects.filter(priority=priority, deleted=False, created_by=request.user.username)
        }[request.user.is_staff]

        serializer = TaskSerializer(tasks_by_priority, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(TaskViewSet, self).list(request, *args, **kwargs)

        user_tasks = Task.objects.filter(deleted=False, created_by=request.user.username)
        serializer = TaskSerializer(user_tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(TaskViewSet, self).retrieve(request, *args, **kwargs)

        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=kwargs['pk'], created_by=request.user.username, deleted=False)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            username = request.user.username
            category_id = request.data.get('category')
            priority_id = request.data.get('priority')
            get_object_or_404(Category.objects.all(), pk=category_id, created_by=username, deleted=False)
            get_object_or_404(Priority.objects.all(), pk=priority_id, created_by=username, deleted=False)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user.username)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff:
            username = request.user.username
            if instance.created_by != username:
                return Response(status=403)
            category_id = request.data.get('category')
            priority_id = request.data.get('priority')
            if category_id:
                get_object_or_404(Category.objects.all(), pk=category_id, created_by=username, deleted=False)
            if priority_id:
                get_object_or_404(Priority.objects.all(), pk=priority_id, created_by=username, deleted=False)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            instance.delete()
        elif not instance.deleted:
            if instance.created_by != request.user.username:
                return Response(status=403)
            instance.deleted = True
            instance.deleted_at = timezone.now()
            instance.save()
        return Response(status=204)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(CategoryViewSet, self).list(request, *args, **kwargs)

        user_categories = Category.objects.filter(deleted=False, created_by=request.user.username)
        serializer = CategorySerializer(user_categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(CategoryViewSet, self).retrieve(request, *args, **kwargs)

        queryset = Category.objects.all()
        task = get_object_or_404(queryset, pk=kwargs['pk'], created_by=request.user.username, deleted=False)
        serializer = CategorySerializer(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user.username)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff:
            username = request.user.username
            if instance.created_by != username:
                return Response(status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            instance.delete()
        elif not instance.deleted:
            if instance.created_by != request.user.username:
                return Response(status=403)
            instance.deleted = True
            instance.deleted_at = timezone.now()
            instance.save()
        return Response(status=204)


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.filter(deleted=False)
    serializer_class = PrioritySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(PriorityViewSet, self).list(request, *args, **kwargs)

        user_priorities = Priority.objects.filter(deleted=False, created_by=request.user.username)
        serializer = PrioritySerializer(user_priorities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(PriorityViewSet, self).retrieve(request, *args, **kwargs)

        queryset = Priority.objects.all()
        task = get_object_or_404(queryset, pk=kwargs['pk'], created_by=request.user.username, deleted=False)
        serializer = PrioritySerializer(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user.username)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff:
            username = request.user.username
            if instance.created_by != username:
                return Response(status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            instance.delete()
        elif not instance.deleted:
            if instance.created_by != request.user.username:
                return Response(status=403)
            instance.deleted = True
            instance.deleted_at = timezone.now()
            instance.save()
        return Response(status=204)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # TODO:
    #  Login (POST)
    #  Logout (POST)
    #  Change password (POST)
    #  Reset password (POST)

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=403)
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(UserViewSet, self).retrieve(request, *args, **kwargs)

        queryset = User.objects.all()
        task = get_object_or_404(queryset, pk=kwargs['pk'], created_by=request.user.username, deleted=False)
        serializer = UserSerializer(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(status=403)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff or instance != request.user:
            return Response(status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff:
            instance.delete()
        elif instance.is_active:
            if request.user != instance:
                return Response(status=403)
            instance.is_active = False
            instance.save()
        return Response(status=204)
