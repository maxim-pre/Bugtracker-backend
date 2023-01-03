from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from.models import Project, Ticket, Developer, ProjectDeveloper, TicketDeveloper, Comment
from django.conf import settings
from.serializers import CreateProjectSerializer, CreateTicketSerializer, DeveloperSerializer, ProjectSerializer, TicketSerializer, UpdateProjectSerializer, CreateProjectDeveloperSerializer, UpdateTicketSerializer, CreateCommentSerializer, CommentSerializer, ProjectDeveloperSerializer, UpdateProjectDeveloperSerializer

# Create your views here.
#you should only be able update and delete the pojects you have created
#you should only be able to view the projects you are assigned to or have created
#when a project is created the creator should automatically be assigned to the project
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Project.objects.select_related().all()

        return Project.objects.select_related().filter(developers__developer__user_id=user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProjectSerializer
        elif self.request.method == 'PATCH' or self.request.method == 'PUT':
            return UpdateProjectSerializer
        return ProjectSerializer
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        developer_id = Developer.objects.only('user_id').get(user_id=request.user.id)
        created_projects = Project.objects.filter(creator_id=developer_id)
        if request.method == 'GET':
            serializer = ProjectSerializer(created_projects, many=True)
            return Response(serializer.data)

        return ProjectSerializer

    
    def destroy(self, request, *args, **kwargs):
        developer_id = Developer.objects.get(user_id=self.request.user.id)
        current_project = Project.objects.get(id=kwargs['pk'])

        if self.request.user.is_staff:
            return super().destroy(request, *args, **kwargs) 

        if current_project.creator != developer_id:
            return Response({'error':'You cannot delete this project because you are not the creator'}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs) 

    def update(self, request, *args, **kwargs):
        developer_id = Developer.objects.get(user_id=self.request.user.id)
        current_project = Project.objects.get(id=kwargs['pk'])

        if current_project.creator != developer_id:
            return Response({'error':'You cannot update this project because you are not the creator'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

class DeveloperViewSet(ModelViewSet):
    queryset = Developer.objects.select_related('user').all()
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['GET','PUT'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        developer = Developer.objects.get(user = request.user.id)
        if request.method == 'GET':
            serializer = DeveloperSerializer(developer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = DeveloperSerializer(developer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class PersonalTicketViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.select_related().all()    

        return Ticket.objects.select_related().filter(developers__developer__user_id=user.id)

    
class TicketViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.select_related().filter(project_id=self.kwargs['project_pk'])

    def get_serializer_context(self):
        return {
            'project_id':self.kwargs['project_pk'],
            'user_id':self.request.user.id,
            }
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTicketSerializer
        
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UpdateTicketSerializer
        return TicketSerializer

    def update(self, request, *args, **kwargs):
        TicketDeveloper.objects.filter(ticket_id=self.kwargs['pk']).delete()
        for id in request.data['developers']:
            TicketDeveloper.objects.create(ticket_id=self.kwargs['pk'], developer_id=id)
        
        request.data.pop('developers')
        return super().update(request, *args, **kwargs)
class ProjectDeveloperViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self): #return the developers in that project
        return ProjectDeveloper.objects.select_related().filter(project_id=self.kwargs['project_pk'])
    
    def get_serializer_context(self):
        return {'project_id':self.kwargs['project_pk']}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProjectDeveloperSerializer
        if self.request.method in ['PUT','PATCH']:
            return UpdateProjectDeveloperSerializer
        return ProjectDeveloperSerializer

    def destroy(self, request, *args, **kwargs):
        developer = Developer.objects.get(id=kwargs['pk'])
        current_project = Project.objects.get(id=kwargs['project_pk'])

        if current_project.creator == developer:
            return Response({'error':'You cannot delete the creator of the project'}, status=status.HTTP_403_FORBIDDEN)

        project_developer = ProjectDeveloper.objects.get(project=current_project, developer=developer)
        self.perform_destroy(project_developer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        return Comment.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        return CommentSerializer

    def get_serializer_context(self):
        return {
            'ticket_id':self.kwargs['ticket_pk'],
            'user_id':self.request.user.id
            }

    def destroy(self, request, *args, **kwargs):
        User = get_user_model()
        username = User.objects.get(id=request.user.id).username
        comment = Comment.objects.get(id=kwargs['pk'])

        if comment.author != username:
            return Response({'error': "you cannot delete comments you haven't made"}, status=status.HTTP_403_FORBIDDEN)
            
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
