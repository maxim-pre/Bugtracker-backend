from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from.models import Project, Ticket, Developer
from.serializers import DeveloperSerializer, ProjectSerializer, TicketSerializer

# Create your views here.
#you should only be able update and delete the pojects you have created
#you should only be able to view the projects you are assigned to or have created
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

#you should only be able to create tickets for the projects you have been assigned to or created
#you can only update and delete the tickets you have made 
class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class DeveloperViewSet(ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

