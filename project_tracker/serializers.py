from django.db import models
from rest_framework import serializers
from .models import Project, ProjectDeveloper, Ticket, Developer, TicketDeveloper, Comment
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        fields = ['id','username','email', 'first_name','last_name']
        model = get_user_model()

class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        fields = ['id', 'user', 'phone', 'birthday',]
        model = Developer
    
class ProjectDeveloperSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer()
    class Meta:
        fields = ['id','developer', 'role', 'admin_permission']
        model = ProjectDeveloper

class UpdateProjectDeveloperSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['id','role','admin_permission']
        model = ProjectDeveloper

class ProjectSerializer(serializers.ModelSerializer):
    creator = DeveloperSerializer()
    developers = ProjectDeveloperSerializer(many=True)
    class Meta:
        fields = ['id', 'name', 'description', 'creator', 'date_created', 'developers']
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
            developer_id=creator.id,
            role='Admin',
            admin_permission=True
        )

class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'description']
        model = Project

class TicketDeveloperSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer()
    class Meta:
        fields = ['developer_id', 'developer']
        model = TicketDeveloper
        extra_kwargs = {
            'developer_id': {'read_only': False}
        }
class UpdateTicketSerializer(serializers.ModelSerializer):
    developers = TicketDeveloperSerializer(many=True)
    class Meta:
        fields = ['title','description','status','priority','type', 'developers']
        model = Ticket

class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Project

class TicketSerializer(serializers.ModelSerializer):
    developers = TicketDeveloperSerializer(many=True)
    submitter = DeveloperSerializer()
    project = SimpleProjectSerializer()
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    
    class Meta:
        fields = ['id', 'title','description','submitter','developers','status', 'type', 'priority','created_at','last_updated','project']
        model = Ticket

    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_type(self, obj):
        return obj.get_type_display()
    
    def get_priority(self, obj):
        return obj.get_priority_display()
        

class CreateTicketSerializer(serializers.ModelSerializer):

    description = serializers.CharField(max_length=255)
    developers = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    class Meta:
        fields = ['title','description', 'developers', 'type','priority']
        model = Ticket

    def save(self, **kwargs):

        submitter = Developer.objects.get(user_id=self.context['user_id'])
        project = Project.objects.get(id=self.context['project_id'])

        new_ticket = Ticket.objects.create(
            project = project,
            submitter = submitter,
            title = self.validated_data['title'],
            description = self.validated_data['description'],
            type = self.validated_data['type'],
            priority = self.validated_data['priority']
        )

        developer_ids = self.validated_data['developers']

        for id in developer_ids:
            TicketDeveloper.objects.create(
                ticket_id = new_ticket.id,
                developer_id = id
            )
        return 


class CreateProjectDeveloperSerializer(serializers.Serializer):
    # developer_id = serializers.IntegerField()
    username = serializers.CharField()
    role = serializers.CharField()
    
    
    def validate_username(self, username):
        User = get_user_model()
        #make sure the user exists
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('developer with that username does not exist')
        #make sure the user is not already part of the project
        user = User.objects.get(username=username)
        developer = Developer.objects.get(user_id=user.id)
        

        invalid_developer_ids = [entry.developer_id for entry in ProjectDeveloper.objects \
                        .only('developer_id') \
                        .filter(project_id=self.context['project_id'])]

        if developer.id in invalid_developer_ids:
            raise serializers.ValidationError(f'{username} is already part of this project')
        
        return username


    
    def save(self, **kwargs):
        # developer_id = self.validated_data['developer_id']
        username = self.validated_data['username']
        role = self.validated_data['role']
        project_id = self.context['project_id']
        
        # find the developer_id based on the provided username
        try:
            User = get_user_model()
            user_id = User.objects.get(username=username).id
            developer = Developer.objects.get(user_id=user_id)
        except:
            raise serializers.ValidationError('A developer with that username does not exist')

        return ProjectDeveloper.objects.create(
            project_id=project_id,
            developer_id = developer.id,
            role=role
        )

        # return ProjectDeveloper.objects.create(
        #     project_id=project_id,
        #     developer_id=developer_id
        # )



class CreateCommentSerializer(serializers.Serializer):
    comment = serializers.CharField()
    def save(self, **kwargs):
        comment = self.validated_data['comment']
        ticket_id = self.context['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)

        user_id = self.context['user_id']
        User = get_user_model()
        user = User.objects.get(id=user_id)
    
        return Comment.objects.create(
                ticket=ticket,
                author=user.username,
                comment=comment
            )
        

class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            fields = ['id','ticket','author','time_created','comment']
            model = Comment

    