from rest_framework import serializers
from . import models

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'description', 'date_created']
        model = models.Project
