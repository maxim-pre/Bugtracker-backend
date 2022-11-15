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

class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'description']
        model = Project
        
class DeveloperSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        fields = ['id', 'user_id', 'phone', 'birthday']
        model = Developer

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title','description','submitter','developer','status','created_at','last_updated','project']
        model = Ticket

class CreateTicketSerializer(serializers.ModelSerializer):
    developer_id = serializers.IntegerField()
    class Meta:
        fields = ['title','description', 'developer_id']
        model = Ticket
    
    def validate_developer_id(self, value):
        if not ProjectDeveloper.objects.filter(project_id=self.context['project_id'], developer_id=value):
            raise serializers.ValidationError('you cannot assign that ticket to a developer that is not part of that project')
        return value

    def save(self, **kwargs):
        submitter = Developer.objects.get(user_id=self.context['user_id'])
        project = Project.objects.get(id=self.context['project_id'])
        developer = self.validated_data['developer_id']

        new_ticket = Ticket.objects.create(
            title = self.validated_data['title'],
            description = self.validated_data['description'],
            submitter = submitter,
            developer_id = developer,
            project = project
        )
        return 

class CreateProjectDeveloperSerializer(serializers.Serializer):
    developer_id = serializers.IntegerField()
    
    def validate_developer_id(self, developer_id):
        #make sure the developer exists
        if not Developer.objects.filter(pk=developer_id).exists():
            raise serializers.ValidationError('error: developer with that id does not exist')
        #make sure the developer is not already part of the project
        invalid_ids = [entry.id for entry in ProjectDeveloper.objects \
                        .only('developer_id') \
                        .filter(project_id=self.context['project_id'])]
        if developer_id in invalid_ids:
            raise serializers.ValidationError(f'error: developer with id {developer_id} is already part of this project')
        
        return developer_id


    
    def save(self, **kwargs):
        developer_id = self.validated_data['developer_id']
        project_id = self.context['project_id']

        return ProjectDeveloper.objects.create(
            project_id=project_id,
            developer_id=developer_id
        )

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'creator', 'date_created']
