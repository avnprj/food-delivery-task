from django.db.models import Q
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser
from .models import *
from .serializers import *


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access if user is admin
        if request.user.is_staff:
            return True
        # Allow access if user is accessing their own profile
        return obj == request.user


class RestaurantViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        location = self.request.query_params.get('location')
        cuisine = self.request.query_params.get('cuisine')

        if cuisine:
            queryset = queryset.filter(menu_items__cuisine__in=[cuisine]).distinct()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if location:
            queryset = queryset.filter(address__icontains=location)

        return queryset


class MenuItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cuisine = self.request.query_params.get('cuisine')
        name = self.request.query_params.get('name')
        location = self.request.query_params.get('location')
        restaurant_id = self.request.query_params.get('restaurant_id')

        if restaurant_id:
            queryset = queryset.filter(restaurant__id=restaurant_id)

        if cuisine:
            queryset = queryset.filter(cuisine__icontains=cuisine)

        if name or location:
            queryset = queryset.filter(
                Q(restaurant__name__icontains=name) |
                Q(restaurant__address__icontains=location)
            )

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        # Retrieve the authenticated user
        user = self.request.user
        queryset = None
        if not user.is_staff:
            # Filter the users based on the authenticated user
            queryset = User.objects.filter(username=user.username)
        else:
            # Filter the users based on the authenticated user
            queryset = User.objects.all()

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Assign the request user to the order
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Retrieve the authenticated user
        user = self.request.user
        queryset = None
        restaurant = self.request.query_params.get('restaurant')

        if user.is_authenticated:
            # Filter the orders based on the authenticated user
            queryset = Order.objects.filter(user=user)

            # Filter the orders based on the restaurant
            queryset = Order.objects.filter(restaurant=restaurant)

        return queryset

