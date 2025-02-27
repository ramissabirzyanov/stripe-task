from rest_framework import serializers
from payment_app.item.models import Item


class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = '__all__'
