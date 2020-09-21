from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views
from django.conf.urls import include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('event/', views.EventList.as_view()),
    path('event/<int:pk>/', views.EventDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)