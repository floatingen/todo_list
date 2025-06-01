from django.shortcuts import render
from rest_framework.views import APIView


class TodoView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'todo/todo.html', {})
