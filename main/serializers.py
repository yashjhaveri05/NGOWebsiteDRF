from rest_framework import serializers
from .models import User,Event,Donation,Redeem,Achievement
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name","last_name","email","mobile_number","address","pancard","coins",]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email","password", "first_name","last_name","mobile_number","address","pancard",)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password = make_password(validated_data['password']),
            first_name = validated_data['first_name'], 
            last_name = validated_data['last_name'], 
            mobile_number = validated_data['mobile_number'],                                      
            address = validated_data['address'], 
            pancard = validated_data['pancard'],
        )
        return user

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=True)
    volunteers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id","title","description","cause","location","duration","event_timings","is_complete","volunteers", "created_by"]

class DonationSerializer(serializers.ModelSerializer):
    donated_by = UserSerializer(many=False,read_only=True)

    class Meta:
        model = Donation
        fields = ["id","donated_by","amount_donated","donated_on","bank_name","bank_branch","payment_method"]

class RedeemSerializer(serializers.ModelSerializer):
    created = UserSerializer(many=False,read_only=True)

    class Meta:
        model = Redeem
        fields = ["id","title","brand","description","price","image","created"]

class AchievementSerializer(serializers.ModelSerializer):
    event = EventSerializer(many=False, read_only=True)

    class Meta:
        model = Achievement
        fields = ["id","event","details","awards","funds_used","image"]
