from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('admin', admin, name="admin"),
    path('login/', login_views, name="login"),
    path('logout/',logout_view,name = 'logout'),
    path('contact/',contact_message,name = 'contact'),
    path('message/',message_list,name = 'message_list'),
    path('projects/',projects_list,name = 'projects_list'),
    path("projects/<int:pk>/delete/", delete_project, name="delete_project"),
    path('logout/', logout_view, name="logout"),
    path('download-cv/', download_cv, name='download_cv'),
    path('add_projects/',add_projects,name = 'add_projects'),
    path('edit_profile/',edit_profile,name = 'edit_profile'),

]
