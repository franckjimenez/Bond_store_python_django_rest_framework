from django.urls import  path
from user_api import views

urlpatterns=[
    path('create/', views.UsersAPIView.as_view())
]