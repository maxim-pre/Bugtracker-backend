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
from.serializers import DeveloperSerializer, ProjectSerializer

# Create your views here.
#you should only be able update and delete the pojects you have created
#you should only be able to view the projects you are assigned to or have created
#when a project is created the creator should automatically be assigned to the project
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
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
    
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        developer_id = Developer.objects.only('user_id').get(user_id=request.user.id)
        created_projects = Project.objects.filter(creator_id=developer_id)
        if request.method == 'GET':
            serializer = ProjectSerializer(created_projects, many=True)
            return Response(serializer.data)



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






