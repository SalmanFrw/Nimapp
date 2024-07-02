from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ClientViewSet, ProjectViewSet, UserViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'users', UserViewSet, basename='user')

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clients/', views.client_list, name='client-list'),
    path('clients/add/', views.client_form, name='client_form'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/delete/', views.client_delete, name='client_delete'),
    path('clients/<int:client_id>/update/', views.client_update, name='client_update'),
    path('projects/', views.project_list, name='project-list'),
    path('projects/add/', views.project_form, name='project_form'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:project_id>/update/', views.project_update, name='project_update'),
    path('users/', views.user_list, name='user-list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('client-form/', views.client_form, name='client-form'),
    path('project-form/', views.project_form, name='project-form'),
    path('user-form/', views.user_form, name='user-form'),
]
