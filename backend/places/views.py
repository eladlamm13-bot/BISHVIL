from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Place, PlaceType
from .serializers import PlaceSerializer, PlaceTypeSerializer

class PlaceTypeViewSet(viewsets.ModelViewSet):
    queryset = PlaceType.objects.all().order_by('display_order')
    serializer_class = PlaceTypeSerializer

    def create(self, request, *args, **kwargs):
        print("Received data from React:", request.data)  # נדפיס את המידע שהגיע
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # נדפיס את השגיאות אם יש
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer