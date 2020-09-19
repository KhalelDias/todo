from django.db import models


class Tasks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False, verbose_name='Done')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

