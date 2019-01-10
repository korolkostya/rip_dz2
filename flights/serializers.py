from .models import Flight
from rest_framework import serializers
from users.views import GetProfileByIdView


class FlightListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('pk', 'flightnumb', 'photo', 'flightfrom', 'flightto', 'price')


class FlightDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('pk', 'flightnumb', 'flightmodel', 'flightfrom', 'flightto', 'slug', 'description', 'photo',
                  'customer', 'bookings', 'price', 'active', 'updated')


    def to_representation(self, instance, *args, **kwargs):
        data = super().to_representation(instance)

        data['customer'] = GetProfileByIdView.as_view()(request=self.context['request']._request,
                                             pk=data['customer']).data

        bookings_cur, data['bookings'] = data['bookings'], []
        for b in bookings_cur:
            r = GetProfileByIdView.as_view()(request=self.context['request']._request,
                                             pk=b)

            data['bookings'].append(
                {
                    'user': r.data
                })
        return data


class FlightDetailEditDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('pk', 'flightnumb', 'flighymodel', 'flightfrom', 'flightto', 'description', 'photo', 'bookings',
                  'price', 'active')
