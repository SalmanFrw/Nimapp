from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class ProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    client_id = serializers.IntegerField()
    users = serializers.CharField(write_only=True, help_text="Comma-separated list of user IDs")
    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_id', 'users', 'created_at', 'created_by']

    def create(self, validated_data):
        client_id = validated_data.pop('client_id')
        users = validated_data.pop('users')
        user_ids = [int(uid) for uid in users.split(',')]
        client = get_object_or_404(Client, pk=client_id)
      
        project = Project.objects.create(client=client, **validated_data)
        project.users.set(User.objects.filter(pk__in=user_ids))
        return project

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = instance.client.client_name
        response['users'] = [{'id': user.id, 'name': user.username} for user in instance.users.all()]
        
        output = {
            'id': response['id'],
            'project_name': response['project_name'],
            'client': response['client'],
            'users': response['users'],
            'created_at': response['created_at'],
            'created_by': response['created_by'],
        }
        
        return output
    

class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%fZ', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        client = Client.objects.create(client_name=validated_data['client_name'], created_by=request.user)
        return client
    
    def update(self, instance, validated_data):
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.updated_by = self.context['request'].user
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        
        if 'projects' in response:
            projects = [
                {'id': project.id, 'name': project.name}
                for project in instance.projects.all()
            ]
            return {
                'id': response['id'],
                'client_name': response['client_name'],
                'projects': projects,
                'created_at': response['created_at'],
                'created_by': response['created_by'],
                'updated_at': response['updated_at']
            }
        else:
            return {
                'id': response['id'],
                'client_name': response['client_name'],
                'created_at': response['created_at'],
                'created_by': response['created_by']
            }



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '_all_'
