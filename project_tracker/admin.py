from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse 
from .models import Project, Ticket





class TicketInLine(admin.TabularInline):
    model = Ticket
    extra=0
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'date_created', 'tickets_count'] # column headers in admin interface
    list_editable = ['description'] 
    date_hierarchy = 'date_created'
    list_per_page = 10
    search_fields = ['name']  
    inlines = [TicketInLine]  

    def tickets_count(self, project):
        url = (reverse('admin:project_tracker_ticket_changelist')  
        + '?'
        + urlencode({'project__id': project.id})
        )
        return format_html('<a href="{}">{} tickets</a>', url, project.tickets_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            tickets_count=Count('ticket')
        )
    

@admin.register(Ticket)
class Tickets(admin.ModelAdmin):
    list_display = ['title', 'project_name', 'submitter', 'created_at', 'developer', 'last_updated', 'status']
    list_select_related = ['project'] #the list of fields we want to eager load
    list_filter = ['project', 'created_at']
    

    def project_name(self, ticket):
        return ticket.project.name


