from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from shapely.geometry import shape, Point


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @method_decorator(ratelimit(key="user", rate="10/s", method="ALL", block=True))
    @action(detail=False, methods=["get"], url_path="contains")
    def contains(self, request):
        lat = float(request.query_params.get("lat"))
        lng = float(request.query_params.get("lng"))
        point = Point(lng, lat)

        areas = []
        for area in ServiceArea.objects.all():
            polygon = shape(area.geojson)
            if polygon.contains(point):
                areas.append(
                    {
                        "polygon_name": area.name,
                        "provider_name": area.provider.name,
                        "price": area.price,
                    }
                )

        return Response(areas)
