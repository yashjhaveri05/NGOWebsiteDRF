from rest_framework import serializers
from .models import User,Event

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