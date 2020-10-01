from django.urls import path
from main import views
from django.conf.urls import include
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #SignUp
    path("register/", views.UserCreate.as_view()),
    #SignIn
    path("login/", views.signin, name="signin"),
    #Logout
    path('logout/', views.Logout.as_view(), name="logout"),
    #Event List View
    path('events/', views.EventList.as_view(), name="events"),
    #Event Create Page
    path('events/new/', views.EventCreate.as_view(), name="event_create"),
    #Event Detail View
    path('events/<int:pk>/', views.EventDetail.as_view(), name="event_detail"),
    #Event Update,Delete
    path('events_crud/<int:pk>/', views.EventCrud.as_view(), name="event_crud"),
    #Donation List
    path('donations/', views.DonationList.as_view(), name="donations"),
    #Donation Made(Make Decision)
    path('mkdonation/', views.donate, name="donate"),
    #Redeem List
    path('redeem/', views.RedeemList.as_view(), name="redeem"),
    #Redeem Create
    path('redeem/new/', views.RedeemCreate.as_view(), name="redeem_create"),
    #Redeem Detail
    path('redeem_detail/<int:pk>/', views.RedeemDetail.as_view(), name="redeem_detail"),
    #Redeem Update,Delete
    path('redeem_crud/<int:pk>/', views.RedeemCrud.as_view(), name="redeem_crud"),
    #Become Volunteer
    path('volunteer/<int:pk>/',views.become_volunteer, name="volunteering"),
    #User Donations For User Dashboard
    path('user_donations/', views.donations_made, name="user_donations"),
    #User Volunteering For User Dashboard
    path('volunteered_in/', views.volunteered_in, name="user_volunteered"),
    #Achievement List View
    path('achievements/', views.AchievementList.as_view(), name="achievements"),
    #Event Detail View
    path('achievements/<int:pk>/', views.AchievementDetail.as_view(), name="achievements_detail"),
    #Event Update,Delete
    path('achievements_crud/<int:pk>/', views.AchievementCrud.as_view(), name="achievements_crud"),
    #Achievement Create
    path('achievement_create/<int:pk>/', views.achievement_create, name="achievements_create")
]