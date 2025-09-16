from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name="index"),
    path('', login_views, name="login"),
    path('logout/',logout_view,name = 'logout'),
    path('contact/',contact_message,name = 'contact'),
    path('logout/', logout_view, name="logout"),
    path('download-cv/', download_cv, name='download_cv'),
]
