from django.urls import path
from main import views
from django.conf.urls import include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('events/', views.EventList.as_view()),
    path('event/new/', views.EventCreate.as_view()),
    path('event_detail/<int:pk>/', views.EventDetail.as_view()),
    path('event_crud/<int:pk>/', views.EventCrud.as_view()),
    path('donations/', views.DonationList.as_view()),
    path('donation/new/', views.DonationCreate.as_view()),
    path('redeem/', views.RedeemList.as_view()),
    path('redeem/new/', views.RedeemCreate.as_view()),
    path('redeem_detail/<int:pk>/', views.RedeemDetail.as_view()),
    path('redeem_crud/<int:pk>/', views.RedeemCrud.as_view()),
]