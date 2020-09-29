from django.shortcuts import render
from rest_framework import generics, status, mixins, permissions
from rest_framework.response import Response
from main.models import User,Event,Donation,Redeem,Achievement
from main.serializers import UserSerializer,EventSerializer,DonationSerializer,RedeemSerializer,AchievementSerializer,RegisterSerializer
from main.permissions import IsOwnerOrReadOnly,IsAdmin,Permit
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
import math
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

"""
User
"""
"""
#SignUp
class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Login
@api_view(["POST"])
def signin(request):
    if request.method == "POST":
        try:
            username = request.data.get("username")
            password = request.data.get("password")  
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                login(request, user)
                data = {
                    "name": user.first_name + " " + user.last_name,
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "mobile_number": user.mobile_number,
                    "Token": token.key,
                }
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(
                data={"Message": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return JsonResponse(
            data={"Message": "Only POST request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        
"""
"""
Events
"""

#Event List View for Everybody(Working)
class EventList(generics.GenericAPIView):

    def get(self, request):
        events = Event.objects.all()
        event_list = EventSerializer(events,many=True).data
        return JsonResponse(event_list, status=status.HTTP_200_OK, safe=False)

#Event Detail Page for Everybody(Working)
class EventDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#Event Create View only for Admin(Working)
class EventCreate(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

#Event Update,Delete for Admin only(Working)
class EventCrud(mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""
Donations
"""

#Donation List for admin only(Working)
class DonationList(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#Donation Made for everybody

#Either this
#need to add permissions and authentication classes(Not Working though before it was)
class DonationCreate(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(donated_by=self.request.user)

#Or this(Not Working)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(["POST"])
def donate(request):
    if request.method == "POST":
        try:
            donated_by = request.user
            amount_donated = request.data.get("amount_donated")
            bank_name = request.data.get("bank_name")
            bank_branch = request.data.get("bank_branch")
            payment_method = request.data.get("payment_method")
            credits_earned = int(0.001*float(amount_donated))
            donation = Donation(donated_by=donated_by,amount_donated=amount_donated,bank_name=bank_name,bank_branch=bank_branch,payment_method=payment_method)
            donation.save()
            users = User.objects.filter(username=donated_by)
            for user in users:
                credit = user.coins + credits_earned
            users.update(coins=credit)
            
        except Exception as e:
            print(e)
            return JsonResponse(
                data={"Message": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return JsonResponse(
            data={"Message": "Only POST request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

"""
Redeem
"""

#Redeem List for everybody
class RedeemList(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#Redeem Detail for everybody
class RedeemDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#Redeem Create for admin
class RedeemCreate(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created=self.request.user)

#Redeem Update,Delete for admin
class RedeemCrud(mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""
Achievements(Left)
"""
#not working
@api_view(['POST'])
def achievement_create(request,pk):
    if request.method == 'POST':
        details = request.data.get("details")
        awards = request.data.get("awards")
        funds_used = request.data.get("funds_used")
        image = request.data.get("image")
        achievement = Achievement.object.create(event=pk,details=details,awards=awards,funds_used=funds_used,image=image)
        serializer = AchievementSerializer(achievement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Achievement List(Working)
class AchievementList(generics.GenericAPIView):
    def get(self, request):
        achievements = Achievement.objects.all()
        achievements_list = AchievementSerializer(achievements,many=True).data
        return JsonResponse(achievements_list, status=status.HTTP_200_OK, safe=False)

#Achievement Detail Page for Everybody(Working)
class AchievementDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#Achievement Update,Delete for Admin only(Working)
class AchievementCrud(mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#Becoming a volunteer button based on event_id(Working if logged in)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['POST'])
def become_volunteer(request,pk):
    user=request.user
    events = Event.objects.filter(pk=pk)
    for event in events:
        event.volunteers.add(user)
    return Response(data={"Message": "Successfully Volunteered For Event"},status=status.HTTP_200_OK)

"""
User Dashboard
"""
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET'])
def donations_made(request):
    if request.method == 'GET':
        donations = Donation.objects.filter(donated_by=request.user)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET'])
def volunteered_in(request):
    volunteers = Event.objects.filter(volunteers=request.user)
    serializer = EventSerializer(volunteers, many=True)
    return Response(serializer.data)