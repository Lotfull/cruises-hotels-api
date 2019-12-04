from rest_framework import generics, serializers

from booking.models import Hotel


class HotelsSerializer(serializers.ModelSerializer):
    room_count = serializers.IntegerField()

    class Meta:
        model = Hotel
        fields = ['id', 'link', 'room_count']


class HotelsAPI(generics.ListAPIView):
    serializer_class = HotelsSerializer

    def get_queryset(self):
        rooms_limit = int(self.request.GET.get('rooms_limit', 20))
        return Hotel.rooms_lt(rooms_limit)
