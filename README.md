# Bugtracker

This an application that helps engineers track and manage software defects and bugs throughout the software development lifecycle. This is a Full-Stack application built using React, Django and MySQL which took me 3 months to complete. This was the first website I built and was a tremendous learning experience for me. Going into this project I only had experience programming in Python, so I had to teach myself JavaScript and the frameworks along the way.

### **Deployment link** : http://bugtrackeradmin.herokuapp.com/

# Getting Started/Code Installation

1. Clone the backend repository by running:

```
$git clone https://github.com/maxim-pre/Bugtracker.git
```

2. Navigate into the settings file and choose a unique password for the database (initially set to just password)

3. Open up MySQL workbench and make a new connection to local host (make sure to set the connection password to the same in django settings)

4. craete a new schema called "bugtracker"

5. inside the Backend run:

```
$pipenv install
$pipenv shell
$python manage.py makemigrations
$python manage.py migrate
```

6. create a new super user by running:

```
$python manage.py createsuperuser
```

7. To start the development server on the backend run"

```
$python manage.py runserver
```

8. clone the front-end repo

```
$git clone https://github.com/maxim-pre/Bugtracker-frontend.git
```

9. navigate to the front-end repo and run:

```

$npm install
$npm run start
```

# Technologies Used

### Stack

- **Django**
- **React**
- **MySQL**
- **Bootstrap**
- **CSS**

### Npm Packages

- **ReCharts** (used to create pie charts)
- **React-Toasify** (used for the notification pop-ups)
- **React-Router**
- **React-Icons**
- **Axios** (HTTP client)

### Gems

- **Devise** (Gem used to implement user authentication)
- **Devise-JWT** (Devise extension to use JWT tokens for Authentication)

### Developer tools

- **Postman**
- **Github**
- **VScode**
- **Pesticide**

# Planning

Considering that this was my first project I didn't really know how to plan it because I didn't really know what I was getting into. However before jumping into the backend I came up with an ERD for the models in the backend.

<img src='images\bugtracker_erd.png'>

# Build/Code Process

The first thing I wanted to implement was the user model which was done using Djoser. The user model was extracted into an app called core. This would be the base application that would be used in all other django apps in this project.

Here I've added a the endpoints provided by djoser

```python
urlpatterns = [
    path('',include('core.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('bugtracker/', include('project_tracker.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
```

Here I've configured the JWT settings to use JWT as the authorization header.

```python
SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
   'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
}
```

Here I've modified Djosers default serializers to include my own fields

```python
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','password','email','first_name','last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username', 'email','first_name','last_name', 'is_staff', 'is_superuser', 'date_joined']

class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username', 'email','first_name','last_name', 'is_staff', 'is_superuser', 'date_joined']
```

The developer model is an extension of the User model in the core app. So, whenever a user Signs up, a signal would be dispatched to create an instance of the developer model

```python
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_developer_for_new_user(sender, instance, created, **kwargs):
    print(instance)
    if created:
        Developer.objects.create(user=instance)
```

Next I started working on implementing the API. Which included creating all necessary models, serializers and views.

Here is an example of the one of the models I created. For the status, priority and type fields I don't what to accept any value, so I'm defining set of choices for each field.

```python
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
```

Here is an example of one of the serializers I created.

The following serializer was used when a user wants to add another contributor to their project. I've made use of django's validate function to make sure that the user being added exists and is not already part of the project.

```python
class CreateProjectDeveloperSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.CharField()


    def validate_username(self, username):
        User = get_user_model()
        #make sure the user exists
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('developer with that username does not exist')
        #make sure the user is not already part of the project
        user = User.objects.get(username=username)
        developer = Developer.objects.get(user_id=user.id)


        invalid_developer_ids = [entry.developer_id for entry in ProjectDeveloper.objects \
                        .only('developer_id') \
                        .filter(project_id=self.context['project_id'])]

        if developer.id in invalid_developer_ids:
            raise serializers.ValidationError(f'{username} is already part of this project')

        return username

    def save(self, **kwargs):
        # developer_id = self.validated_data['developer_id']
        username = self.validated_data['username']
        role = self.validated_data['role']
        project_id = self.context['project_id']

        # find the developer_id based on the provided username
        try:
            User = get_user_model()
            user_id = User.objects.get(username=username).id
            developer = Developer.objects.get(user_id=user_id)
        except:
            raise serializers.ValidationError('A developer with that username does not exist')

        return ProjectDeveloper.objects.create(
            project_id=project_id,
            developer_id = developer.id,
            role=role
        )
```

Here is an example of one of the views I created

Here I'm inheriting the ModelViewSet class which comes with a set of default actions for performing CRUD actions, which removed a lot of boiler plate code.

```python
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
```

# Challenges

-

# Wins

# Key Learnings/Takeaways

# Bugs Future improvements
