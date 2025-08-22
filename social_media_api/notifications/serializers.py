from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor_details = UserSerializer(source='actor', read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'actor_details', 'verb', 'timestamp', 'is_read', 'target')
        read_only_fields = ('id', 'timestamp')

