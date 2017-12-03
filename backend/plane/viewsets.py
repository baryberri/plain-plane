import json
from django.forms.models import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from user.models import User
from .models import Plane


class PlaneViewSet(viewsets.ModelViewSet):
    @list_route(methods=['post'])
    def write_plane(self, request):
        req_data = json.loads(request.body.decode())
        content = req_data['content']
        latitude = req_data['latitude']
        longitude = req_data['longitude']
        tag = req_data['tag']

        author = User.objects.get(user=request.user)

        new_plane = Plane(author=author, content=content,
                          is_replied=False, is_reported=False,
                          latitude=latitude, longitude=longitude, tag=tag)
        new_plane.set_expiration_date()
        new_plane.save()

        author.decrease_today_write()

        return Response(status=status.HTTP_201_CREATED)

    @list_route(url_path="(?P<plane_id>[0-9]+)", methods=['get', 'put'])
    def plane_detail(self, request, plane_id):
        if request.method == "GET":
            plane_id = int(plane_id)
            try:
                plane = Plane.objects.get(id=plane_id)
            except Plane.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            d = model_to_dict(plane)
            return Response(d)

            # Set is_replied
        elif request.method == 'PUT':
            try:
                plane = Plane.objects.get(id=plane_id)
            except Plane.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            plane.set_is_replied(True)
            plane.save()
            return Response(status=status.HTTP_200_OK)

    @list_route(url_path="random")
    def get_random_plane(self, request):
        random_planes = Plane.objects.all().order_by('?')[:6]

        # Serialize randomPlanes
        dict_random_planes = []
        for random_plane in random_planes:
            d = model_to_dict(random_plane)
            dict_random_planes.append(d)

        return Response(dict_random_planes)

    # TODO: getNearPlane()
