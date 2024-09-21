from django.utils import timezone
from rest_framework import serializers
from .models import Task, Category, Priority


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'deleted_at', 'deleted')

    def update(self, instance, validated_data):
        if validated_data.get('is_completed'):
            instance.completed_at = timezone.now()
        else:
            instance.completed_at = None
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'deleted')


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'deleted_at', 'deleted')
