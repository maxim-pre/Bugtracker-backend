from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

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
    submitter = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
