from rest_framework import status
from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Properties
from rest_framework import generics


from core.api.serializers.core_serializers import (
    PropertySerializer, PropertyRetrieveSerializer
)



from rest_framework import generics
from django_filters import rest_framework as filters
from core.admin import Properties

class UserListView(generics.ListAPIView):
    
    filter_backends = [DjangoFilterBackend]

class PropertyList(generics.ListAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name')


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    parser_classes = (JSONParser, MultiPartParser, )


    
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter()
        return self.get_serializer().Meta.model.objects.filter(id=pk).first()
    
    

    def list(self, request):
        property_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "totalNotFiltered": self.get_queryset().count(),
            "rows": property_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        # send information to serializer 
        serializer = self.get_serializer(data=request.data)     
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Property succesfully created!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        properties = self.get_queryset(pk)
        if properties:
            property_serializer = PropertyRetrieveSerializer(properties)
            return Response(property_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'property doesnt exist!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            # send information to serializer referencing the instance
            #data = validate_files(request.data, 'image', True)
            property_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)            
            if property_serializer.is_valid():
                property_serializer.save()
                return Response({'message':'Property succesfully updated!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':property_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        properties = self.get_queryset().filter(id=pk).first() # get instance        
        if properties:
            properties.save()
            return Response({'message':'property destroy succesfully!'}, status=status.HTTP_200_OK)
        return Response({'error':'property doesnt exist!'}, status=status.HTTP_400_BAD_REQUEST)