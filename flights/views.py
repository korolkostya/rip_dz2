from .serializers import FlightListSerializer, FlightDetailSerializer, FlightDetailEditDeleteSerializer
from .models import Flight
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import (ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


class FlightListView(ListAPIView):
    queryset = Flight.objects.filter(active=True)
    serializer_class = FlightListSerializer


class FlightMineListView(ListAPIView):
    serializer_class = FlightListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Flight.objects.filter(customer=self.request.user)


class FlightDetailView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FlightDetailSerializer

    queryset = Flight.objects.filter(active=True)


class FlightUpdateView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)

    queryset = Flight.objects.all()
    serializer_class = FlightDetailEditDeleteSerializer


class FlightDeleteView(DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated,)

    queryset = Flight.objects.all()
    serializer_class = FlightDetailSerializer


class FlightCreateView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Flight.objects.all()
    serializer_class = FlightDetailEditDeleteSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class AddToBookingsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Flight.objects.all()
    serializer_class = FlightDetailEditDeleteSerializer

    def post(self, request, pk):
        obj = Flight.objects.get(pk=pk)
        obj.bookings.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
