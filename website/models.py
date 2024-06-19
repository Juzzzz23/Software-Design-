from django.db import models
from django.contrib.auth.models import User

#GAWA NG FIELDS OR TABLES 
#class Table(models.Model):

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    task = models.CharField(max_length=255)
    due_date = models.DateField()
    due_time = models.TimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task
