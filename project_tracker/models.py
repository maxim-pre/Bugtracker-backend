from django.db import models
from django.contrib import admin
from django.conf import settings

class Developer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(Developer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']
class ProjectDeveloper(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

    def developer_name(self):
        return f'{self.developer.user.first_name} {self.developer.user.last_name}'
    
    def project_title(self):
        return self.project.name
    
    class Meta:
        unique_together=['project','developer']
    


class Ticket(models.Model):
    STATUS_OPEN = 'O'
    STATUS_STARTED = 'S'
    STATUS_CLOSED = 'C'
    
    STATUS_CHOICES = [
        (STATUS_OPEN, 'open'),
        (STATUS_STARTED, 'started'),
        (STATUS_CLOSED, 'closed')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    submitter = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='submitter')
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='developer')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def project_name(self):
        return self.project.name
    def submitter_name(self):
        return f'{self.submitter.user.first_name} {self.submitter.user.last_name}'
    def developer_name(self):
        return f'{self.developer.user.first_name} {self.developer.user.last_name}'
