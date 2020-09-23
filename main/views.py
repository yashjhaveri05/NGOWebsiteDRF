from django.shortcuts import render
from rest_framework import generics, status, mixins, permissions
from rest_framework.response import Response
from main.models import User,Event,Donation,Redeem,Achievement
from main.serializers import UserSerializer,EventSerializer,DonationSerializer,RedeemSerializer,AchievementSerializer,RegisterSerializer
from main.permissions import IsOwnerOrReadOnly,IsAdmin,Permit
from rest_framework.decorators import api_view,authentication_classes
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
import math

"""
User
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

"""
Events
"""

#Event List View for Everybody
class EventList(generics.GenericAPIView):

    def get(self, request):
        events = Event.objects.all()
        event_list = EventSerializer(events,many=True).data
        return JsonResponse(event_list, status=status.HTTP_200_OK, safe=False)

#Event Detail Page for Everybody
class EventDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

#Event Create View only for Admin
class EventCreate(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

#Event Update,Delete for Admin only
class EventCrud(mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""
Donations
"""

#Donation List for admin only
class DonationList(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#Donation Made for everybody

#Either this
#need to add permissions and authentication classes
class DonationCreate(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(donated_by=self.request.user)

#Or this
#need to add permissions and authentication classes
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

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

"""
Achievements(Left)
"""

@api_view(['POST'])
def achievement_create(request):
    if request.method == 'POST':
        serializer = AchievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AchievementList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#Becoming a volunteer button based on event_id(need to check)
#need to add permissions and authentication classes
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
#need to add permissions and authentication classes
@api_view(['GET'])
def donations_made(request):
    if request.method == 'GET':
        donations = Donation.objects.filter(donated_by=request.user)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

#need to add permissions and authentication classes
@api_view(['GET'])
def volunteered_in(request,pk):
    volunteers = Event.objects.filter(volunteers=request.user)
    serializer = EventSerializer(volunteers, many=True)
    return Response(serializer.data)