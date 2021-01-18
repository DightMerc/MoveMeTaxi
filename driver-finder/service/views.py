from django.shortcuts import render

from rest_framework.schemas.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core import models

import json
import random


class FindClosestDriver(APIView):

    def post(self, request):

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            location = data['location']
        except Exception as e:
            return Response(
                'location is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            latitude = location['latitude']
            latitude = location['longitude']
        except Exception as e:
            return Response(
                'location format is wrong',
                status=status.HTTP_400_BAD_REQUEST
                )

        driver = models.Driver.objects.all()

        return Response(
            {
                'drivers': [

                ]
            },
            status=status.HTTP_200_OK
        )
