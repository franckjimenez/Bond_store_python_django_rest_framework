from django.urls import  path

from user_api import views


""" user_data_list= views.UserSerializer.as_view({
    {'get','list'}
}) """

urlpatterns=[
    path('hello/', views.HelloView.as_view()),
    # path('users/', user_data_list),
    path('getusers/', views.UsersAPIView.as_view())
]