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
            tasks = Tasks.objects.get(owner=request.user.id)
        except Tasks.DoesNotExist:
            return Response({})
        serializer = TasksSerializer(tasks)
        return Response(serializer.data)

    # TODO
    def post(self, request):
        serializer = TasksSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TasksDetail(APIView):
    def get_object(self, pk):
        try:
            return Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TasksSerializer(task)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        task = self.get_object(pk)
        serializer = TasksSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="wrong parameters")
