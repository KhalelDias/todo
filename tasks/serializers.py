from rest_framework import serializers
from tasks.models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('title', 'description', 'due_date', 'is_done',)

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['owner'] = user
        return attrs
