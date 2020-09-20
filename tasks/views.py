from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.models import Tasks
from tasks.serializers import TasksSerializer
from .tasks import send_email_execute


@api_view(('POST',))
def mark_done(request, pk):
    try:
        task = Tasks.objects.get(pk=pk)
        done_undone = 'done'
        if task.is_done is False:
            task.is_done = True
        else:
            task.is_done = False
            done_undone = 'undone'
        task.save()
        send_email_execute.delay(request.user.email, task.title, done_undone)
        return Response(TasksSerializer(task).data)
    except Tasks.DoesNotExist:
        raise Http404


class TasksList(APIView):

    def get(self, request):
        try:
            tasks = Tasks.objects.filter(owner=request.user)
        except Tasks.DoesNotExist:
            return Response({})
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TasksSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TasksDetail(APIView):

    def get_object(self, request, pk):
        try:
            task = Tasks.objects.get(pk=pk)
            if task.owner == request.user:
                return task
            else:
                return None
        except Tasks.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(request, pk)
        if task is None:
            return Response('You do not have an access to proceed this action', status=status.HTTP_403_FORBIDDEN)
        serializer = TasksSerializer(task)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        task = self.get_object(request, pk)
        if task is None:
            return Response('You do not have an access to proceed this action', status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        task = self.get_object(request, pk)
        if task is None:
            return Response('You do not have an access to proceed this action', status=status.HTTP_403_FORBIDDEN)
        serializer = TasksSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="wrong parameters")
