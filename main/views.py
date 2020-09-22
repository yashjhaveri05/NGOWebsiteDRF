from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from main.models import User,Event,Donation,Redeem
from main.serializers import UserSerializer,EventSerializer,DonationSerializer,RedeemSerializer
from rest_framework import permissions
from main.permissions import IsOwnerOrReadOnly,IsAdmin
from rest_framework import mixins
from rest_framework.decorators import api_view
from django.http import JsonResponse

"""
@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

class UserList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdmin]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
class DonationCreate(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(donated_by=self.request.user)

"""
Redeem
"""

#Redeem List for everybody
class RedeemList(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#Redeem Detail for everybody
class RedeemDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Redeem.objects.all()
    serializer_class = RedeemSerializer

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