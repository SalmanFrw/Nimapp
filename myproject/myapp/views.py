from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.models import User
from .forms import ClientForm, ProjectForm, UserForm


def home(request):
    clients = Client.objects.all()
    return render(request, 'home.html', {'clients': clients})

def client_form(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_form.html', {'form': form})

def project_form(request):
    return render(request, 'project_form.html')


def user_form(request):
    return render(request, 'user_form.html')

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'client_detail.html', {'client': client})


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'client_delete.html', {'client': client})


def client_update(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, 'client_form.html', {'form': form})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_detail.html', {'project': project})

def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project-list')
    return render(request, 'project_delete.html', {'project': project})



def project_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('project-list')
    return render(request, 'project_form.html', {'form': form})

def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password)
            return redirect('user-list')  # Assuming 'user-list' is the name of the view to list users
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'user_detail.html', {'user': user})

def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')
    return render(request, 'user_delete.html', {'user': user})

def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = [
            {
                'id': item['id'],
                'client_name': item['client_name'],
                'created_at': item['created_at'],
                'created_by': item['created_by']
            }
            for item in serializer.data
        ]
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Customizing the output format
        data = [
            {
                'id': item['id'],
                'project_name': item['project_name'],
                'client_name': item['client'],
                'created_at': item['created_at'],
                'created_by': item['created_by']
            }
            for item in serializer.data
        ]
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Customizing the output format
        data = {
            'id': serializer.data['id'],
            'project_name': serializer.data['project_name'],
            'client_name': serializer.data['client'],
            'created_at': serializer.data['created_at'],
            'created_by': serializer.data['created_by']
        }
        return Response(data)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new User
        user = User.objects.create_user(username=username, password=password)
       
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
