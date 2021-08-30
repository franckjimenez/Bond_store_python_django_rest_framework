from django.urls import  path

from bond_api import views

# bond_data_list= views.BondsView.as_view({
#      {'get','list'}
# })


urlpatterns=[
    #path('hello/', views.HelloView.as_view()),
    path('bonds/',views.BondsAPIView.as_view()),
    path('bonds/usd',views.BondsDollarsAPIView.as_view()),
    path('sell_bonds/',views.Sell_BondsAPIView.as_view()),
    path('buy_bonds/',views.Buy_BondsAPIView.as_view()),
]