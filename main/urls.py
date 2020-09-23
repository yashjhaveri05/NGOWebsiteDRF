from django.urls import path
from main import views
from django.conf.urls import include

urlpatterns = [
    #SignUp
    path("register/", views.UserCreate.as_view()),
    #SignIn
    path("login/", views.signin, name="signin"),
    #path("Logout", views.Logout, name="Logout"),
    #Event List View
    path('events/', views.EventList.as_view()),
    #Event Create Page
    path('event/new/', views.EventCreate.as_view()),
    #Event Detail View
    path('event_detail/<int:pk>/', views.EventDetail.as_view()),
    #Event Update,Delete
    path('event_crud/<int:pk>/', views.EventCrud.as_view()),
    #Donation List
    path('donations/', views.DonationList.as_view()),
    #Donation Made(Make Decision)
    path('donate/', views.DonationCreate.as_view()),
    path('mkdonation/', views.donate),
    #Redeem List
    path('redeem/', views.RedeemList.as_view()),
    #Redeem Create
    path('redeem/new/', views.RedeemCreate.as_view()),
    #Redeem Detail
    path('redeem_detail/<int:pk>/', views.RedeemDetail.as_view()),
    #Redeem Update,Delete
    path('redeem_crud/<int:pk>/', views.RedeemCrud.as_view()),
    #Become Volunteer
    path('volunteer/',views.become_volunteer),
    #User Donations For User Dashboard
    path('user_donations/', views.donations_made),
    #User Volunteering For User Dashboard
    path('volunteered_in/', views.volunteered_in),
    #To Be Done: achievements CRUD,Logout,Others,Check if others work
]