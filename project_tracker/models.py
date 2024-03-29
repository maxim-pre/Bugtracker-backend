from django.db import models
from django.contrib import admin
from django.conf import settings

class Developer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='developer')
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='developers')
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='project_developers')
    role = models.CharField(max_length=255, default="Developer")
    admin_permission = models.BooleanField(default=False)

    def developer_name(self):
        return f'{self.developer.user.first_name} {self.developer.user.last_name}'
    
    def developer_username(self):
        return f'{self.developer.user.username}'
    
    def project_title(self):
        return self.project.name
    
    class Meta:
        unique_together=['project','developer']
    

class Ticket(models.Model):
    STATUS_OPEN = 'O'
    STATUS_STARTED = 'S'
    STATUS_CLOSED = 'C'

    TYPE_ISSUE = 'I'
    TYPE_BUG = 'B'
    TYPE_FEATURE_REQUEST = 'FR'

    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'

    STATUS_CHOICES = [
        (STATUS_OPEN, 'open'),
        (STATUS_STARTED, 'started'),
        (STATUS_CLOSED, 'closed')
    ]

    TYPE_CHOICES = [
        (TYPE_ISSUE, 'issue'),
        (TYPE_BUG, 'bug'),
        (TYPE_FEATURE_REQUEST, 'feature request'),
    ]

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'low'),
        (PRIORITY_MEDIUM, 'medium'),
        (PRIORITY_HIGH, 'high'),
    ]


    title = models.CharField(max_length=255)
    description = models.TextField()
    submitter = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='submitter')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_OPEN)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=TYPE_ISSUE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def project_name(self):
        return self.project.name
    def submitter_name(self):
        return f'{self.submitter.user.first_name} {self.submitter.user.last_name}'
    def developer_name(self):
        return f'{self.developer.user.first_name} {self.developer.user.last_name}'

class TicketDeveloper(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='developers')
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

    def developer_name(self):
        return f'{self.developer.user.first_name} {self.developer.user.last_name}'
    
    def ticket_title(self):
        return self.ticket.name
    
    class Meta:
        unique_together=['ticket','developer']

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


    