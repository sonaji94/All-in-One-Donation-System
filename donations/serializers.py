from rest_framework import serializers
from .models import Donation
from accounts.serializers import UserSerializer

class DonationSerializer(serializers.ModelSerializer):
    donor_info = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ('donor', 'status', 'payment_id', 'created_at')

    def get_donor_info(self, obj):
        if obj.is_anonymous:
            return {"name": "Anonymous"}
        if obj.donor:
            return {"name": obj.donor.username}
        return {"name": "Guest"}

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
        return super().create(validated_data)
