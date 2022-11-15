from multiprocessing import context
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from.models import Project, Ticket, Developer, ProjectDeveloper
from django.conf import settings
from.serializers import CreateProjectSerializer, CreateTicketSerializer, DeveloperSerializer, ProjectSerializer, TicketSerializer, UpdateProjectSerializer, CreateProjectDeveloperSerializer, TestSerializer

# Create your views here.
#you should only be able update and delete the pojects you have created
#you should only be able to view the projects you are assigned to or have created
#when a project is created the creator should automatically be assigned to the project
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if self.request.user.is_staff:
            return Project.objects.all()

        developer_id = Developer.objects.only('id').get(user_id=user.id)
        related_projects = ProjectDeveloper.objects.select_related('project').only('project_id').filter(developer_id=developer_id)
        project_ids = [i.project_id for i in related_projects]
        return Project.objects.filter(id__in=project_ids)

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

        if current_project.creator != developer_id:
            return Response({'error':'You cannot delete this project because you are not the creator'})
        
        return super().destroy(request, *args, **kwargs) 

class DeveloperViewSet(ModelViewSet):
    queryset = Developer.objects.all()
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

class TicketViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(project_id=self.kwargs['project_pk'])
    
    def get_serializer_context(self):
        return {
            'project_id':self.kwargs['project_pk'],
            'user_id':self.request.user.id,
            }
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTicketSerializer
        return TicketSerializer

class ProjectDeveloperViewSet(ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self): #return the developers in that project
        developer_list = ProjectDeveloper.objects.filter(project_id=self.kwargs['project_pk'])
        developer_ids = [entry.developer_id for entry in developer_list]
        return Developer.objects.filter(id__in=developer_ids)
    
    def get_serializer_context(self):
        return {'project_id':self.kwargs['project_pk']}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProjectDeveloperSerializer
        return DeveloperSerializer

class TestViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = TestSerializer
    




