from django.db import models
from rest_framework import serializers
from .models import Project, Ticket, Developer
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'creator', 'date_created']
        model = Project

class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name','description']
        model = Project

class DeveloperSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        fields = ['id', 'user_id', 'phone', 'birthday']
        model = Developer
