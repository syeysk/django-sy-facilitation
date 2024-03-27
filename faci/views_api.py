from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from faci.models import FaciCanvas
from faci.serializers_api import (
    AddFaciViewSerializer,
    GetListFaciSerializer,
)

FACI_CREATOR_FOR_WHAT = 'Инициатор встречи'


class AddFaciView(APIView):
    AIM_TYPES = {
        'solution': FaciCanvas.AIM_TYPE_SOLUTION,
        'idea': FaciCanvas.AIM_TYPE_IDEA,
        'sync': FaciCanvas.AIM_TYPE_SYNC,
    }

    def post(self, request):
        serializer = AddFaciViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        faci = FaciCanvas(
            aim=data['aim'],
            if_not_reached=data['if_not_reached'],
            aim_type=self.AIM_TYPES[data['aim_type']],
            solutions=data['solutions'],
        )
        faci.save()
        data_for_return = {'id': faci.pk}
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class GetListFaciView(APIView):
    def get(self, request):
        serializer = GetListFaciSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        facis = (
            FaciCanvas.objects.all().order_by('-id')
            .values('id', 'aim', 'if_not_reached', 'aim_type')
        )
        facis = facis[(data['page_number']-1)*data['count_on_page']:data['count_on_page']]

        data_for_return = {
            'facis': facis,
            'total': FaciCanvas.objects.count(),
        }
        return Response(status=status.HTTP_200_OK, data=data_for_return)
