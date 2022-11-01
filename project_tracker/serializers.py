from django.db import models
from rest_framework import serializers
from .models import Project, ProjectDeveloper, Ticket, Developer



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'creator', 'date_created']
        model = Project

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']
    
    def save(self, **kwargs):
        creator = Developer.objects.get(user_id=self.context['user_id'])
        new_project = Project.objects.create(
            name = self.validated_data['name'],
            description = self.validated_data['description'],
            creator = creator
        )
        #automatically assign the project creator to the list of developers
        ProjectDeveloper.objects.create(
            project_id=new_project.id,
            developer_id=creator.id
        )
        
class DeveloperSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        fields = ['id', 'user_id', 'phone', 'birthday']
        model = Developer
        
