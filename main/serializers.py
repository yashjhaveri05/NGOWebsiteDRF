from rest_framework import serializers
from .models import User,Event,Donation,Redeem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","first_name","last_name","email","mobile_number","address","pancard","coins",]

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