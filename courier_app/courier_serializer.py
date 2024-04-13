from rest_framework import serializers
from .models import Product, Order, OrderDetail
from rest_framework.serializers import ModelSerializer
from user_auth.user_serializer import UserListingSerializer

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = UserListingSerializer(instance.created_by).data if instance.created_by else None
        data['updated_by'] = UserListingSerializer(instance.updated_by).data if instance.updated_by else None
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['updated_at']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_at_date'] = instance.created_at.date()
        data['order_details'] = OrderDetailSerializer(instance.order_detail_order.all(), many=True).data if instance.order_detail_order else None
        return data

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

    

    