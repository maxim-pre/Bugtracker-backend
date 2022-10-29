from rest_framework import serializers
from .models import Project, Ticket

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'date_created']
        model = Project

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','title','description','submitter','developer','status','created_at','last_updated','project']
        model = Ticket
