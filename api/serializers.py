from rest_framework import serializers
from .models import Restaurant, MenuItem, User, Order
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'email']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'restaurant', 'price', 'photo']

class UserSerializer(serializers.ModelSerializer):
    tokens = TokenObtainPairSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'delivery_address', 'tokens']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            delivery_address=validated_data['delivery_address']
        )
        return user


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'menu_items', 'quantity', 'total_price']

    def create(self, validated_data):
        menu_items_data = validated_data.pop('menu_items')
        order = Order.objects.create(**validated_data)
        order.menu_items.set(menu_items_data)
        return order
