from django.shortcuts import render

from rest_framework.schemas.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core import models
import api.serializers as serializers


class CompanyView(APIView):

    def get(self, request, version):

        if version == 'v1':

            all = models.Company.objects.all()

            content = serializers.CompanySerializer(all, many=True).data
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )

        else:

            content = []
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )


class StatusView(APIView):

    def get(self, request, version):

        if version == 'v1':

            all = models.Status.objects.all()

            content = serializers.StatusSerializer(all, many=True).data
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )

        else:

            content = []
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )


class InvoiceView(APIView):

    def get(self, request, version):

        if version == 'v1':

            all = models.Invoice.objects.all()

            content = serializers.InvoiceSerializer(all, many=True).data
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )

        else:

            content = []
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )


class GoodView(APIView):

    def get(self, request, version):

        if version == 'v1':

            all = models.Good.objects.all()

            content = serializers.GoodSerializer(all, many=True).data
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )

        else:

            content = []
            response_status = status.HTTP_200_OK

            return Response(
                {
                    'content': content
                },
                status=response_status
            )
