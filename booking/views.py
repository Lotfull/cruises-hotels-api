from rest_framework import generics, views, serializers
from rest_framework.response import Response
from booking.core.cruises import get_cruises


from booking.models import Hotel


def cruises(request):
    context = dict()
    params = request.POST or request.GET
    try:
        context = get_cruises(params.get('num', 4))
    except Exception as e:
        context['error_message'] = str(e)

    return context


class CruisesAPI(views.APIView):
    def get(self, request):
        return Response(cruises(request))


class HotelsSerializer(serializers.ModelSerializer):
    room_count = serializers.IntegerField()

    class Meta:
        model = Hotel
        fields = ['id', 'link', 'room_count']


class HotelsAPI(generics.ListAPIView):
    serializer_class = HotelsSerializer

    def get_queryset(self):
        rooms_limit = int(self.request.GET.get('room_limit', 20))
        return Hotel.rooms_lt(rooms_limit)
