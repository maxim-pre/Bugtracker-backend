from django.db import models
from rest_framework import serializers
from .models import Project, Ticket, Developer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'description', 'date_created']
        model = Project

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','title','description','submitter','developer','status','created_at','last_updated','project']
        model = Ticket

class DeveloperSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        fields = ['id', 'user_id', 'phone', 'birthday']
        model = Developer
