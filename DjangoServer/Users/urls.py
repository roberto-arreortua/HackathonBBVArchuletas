from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('', UsersCRUD.as_view(),name='user_crud'),
    path('login/', Login.as_view(),name='user_login'),
    path('speechrecognition/', VoiceRecognition.as_view(),name='user_login'),
    path('login_archu/', LoginBBVArchuletas.as_view(),name='archuleta_login'),
    path('information/', UsersInformation.as_view(),name='archuleta_login'),
    
]

#Custom titles for admin
from django.contrib import admin
admin.site.site_header = "BBVA Archuletas"
admin.site.index_title = "Chinpances"
admin.site.site_title="BBVA Archuletas"