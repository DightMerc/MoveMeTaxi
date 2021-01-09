from django.shortcuts import render

from rest_framework.schemas.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core import models
import api.serializers as serializers

import json
import random


class DeviceView(APIView):

    def get(self, request, version):
        device_list = models.Device.objects.all()
        return Response(
            serializers.DeviceSerializer(device_list, many=True).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, version):

        data = json.loads(request.body)

        try:
            device_type = str(data['device_type'])
        except Exception as e:
            return Response(
                'device_type is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        if models.DeviceType.objects.filter(title=device_type).count() == 0:
            return Response(
                'no selected device_type found',
                status=status.HTTP_404_NOT_FOUND
                )
        else:
            DeviceType = models.DeviceType.objects.get(title=device_type)

        NewDevice = models.Device()

        NewDevice.type = DeviceType

        NewDevice.save()

        content = serializers.DeviceSerializer(NewDevice).data

        return Response(
            {
                'content': content
            },
            status=status.HTTP_201_CREATED
            )


class AuthDeviceView(APIView):

    def post(self, request, version, GUID):

        data = json.loads(request.body)

        try:
            Device = models.Device.objects.get(GUID=GUID)
        except models.Device.DoesNotExist:
            return Response(
                'device with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        if not Device.active:
            return Response(
                'device with selected GUID is inactive',
                status=status.HTTP_403_FORBIDDEN
                )

        try:
            phone = str(data['phone'])
        except Exception as e:
            return Response(
                'phone is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        if not phone.isdigit():
            return Response(
                'wrong data format',
                status=status.HTTP_400_BAD_REQUEST
                )

        verification_code = random.randint(100000, 999999)

        Device.verification_code = verification_code
        Device.save()

        # TODO
        """
            sms_service.sendMessage(phone, verification code)
        """

        try:
            CoreUser = models.CoreUser.objects.get(phone=phone)
        except models.CoreUser.DoesNotExist:
            CoreUser = models.CoreUser()
            CoreUser.email = ''
            CoreUser.language = models.Language.objects.get(id=1)
            CoreUser.phone = phone
            CoreUser.firstname = ''
            CoreUser.surname = ''
            CoreUser.photo = models.ProfilePhoto.objects.get(id=1)
            CoreUser.status = models.UserStatus.objects.get(id=1)
            CoreUser.save()

        CoreUser.devices.add(Device)

        return Response(
            'verification code sent: ' + str(verification_code),
            status=status.HTTP_200_OK
        )


class AuthDeviceCheckView(APIView):

    def post(self, request, version, GUID):

        data = json.loads(request.body)

        try:
            Device = models.Device.objects.get(GUID=GUID)
        except models.Device.DoesNotExist:
            return Response(
                'device with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        if not Device.active:
            return Response(
                'device with selected GUID is inactive',
                status=status.HTTP_403_FORBIDDEN
                )

        try:
            code = str(data['code'])
        except Exception as e:
            return Response(
                'code is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        if not code.isdigit():
            return Response(
                'wrong data format',
                status=status.HTTP_400_BAD_REQUEST
                )

        if Device.verification_code == code:
            Device.verified = True
            Device.save()
        else:
            return Response(
                'wrong verification code',
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            CoreUser = models.CoreUser.objects.get(devices=Device)
            driver = models.Driver.objects.get(user=CoreUser)
            for device in CoreUser.devices.all():
                if device.id != Device.id:
                    device.active = False
                    device.save()
        except Exception as e:
            pass

        return Response(
            'accepted',
            status=status.HTTP_202_ACCEPTED
        )


class LanguageListView(APIView):

    def get(self, request, version):

        return Response(
            serializers.LanguageSerializer(models.Language.objects.all(), many=True).data
        )


class UserView(APIView):

    def get(self, request, version, GUID):

        try:
            Device = models.Device.objects.get(GUID=GUID)
        except models.Device.DoesNotExist:
            return Response(
                'device with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        if not Device.active:
            return Response(
                'device with selected GUID is inactive',
                status=status.HTTP_403_FORBIDDEN
                )

        try:
            CoreUser = models.CoreUser.objects.get(devices=Device)
        except models.CoreUser.DoesNotExist:
            return Response(
                'user not found',
                status=status.HTTP_404_NOT_FOUND
            )

        found = False

        try:
            user = models.Client.objects.get(user=CoreUser)
            found = 'client'
        except models.Client.DoesNotExist:
            pass

        try:
            user = models.Driver.objects.get(user=CoreUser)
            found = 'driver'
        except models.Driver.DoesNotExist:
            pass

        if not found:
            return Response(
                'core user exists, but type of user not set',
                status=status.HTTP_404_NOT_FOUND
            )
        elif found == 'client':
            result = serializers.ClientSerializer(user).data
            result['type'] = 'client'
        elif found == 'driver':
            result = serializers.DriverSerializer(user).data
            result['type'] = 'driver'

        return Response(
            result,
            status=status.HTTP_200_OK
        )

    def post(self, request, version, GUID):

        data = json.loads(request.body)

        try:
            Device = models.Device.objects.get(GUID=GUID)
        except models.Device.DoesNotExist:
            return Response(
                'device with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        if not Device.active:
            return Response(
                'device with selected GUID is inactive',
                status=status.HTTP_403_FORBIDDEN
                )

        try:
            CoreUser = models.CoreUser.objects.get(devices=Device)
        except models.CoreUser.DoesNotExist:
            return Response(
                'user not found',
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            email = str(data['email'])
        except Exception as e:
            email = ''

        try:
            language = str(data['language'])
        except Exception as e:
            return Response(
                'language is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            language = models.Language.objects.get(title=language)
        except Exception as e:
            return Response(
                'selected language not found',
                status=status.HTTP_404_NOT_FOUND
                )

        try:
            phone = str(data['phone'])
        except Exception as e:
            return Response(
                'phone is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        if not phone.isdigit():
            return Response(
                'wrong data format: phone',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            firstname = str(data['firstname'])
        except Exception as e:
            return Response(
                'firstname is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            surname = str(data['surname'])
        except Exception as e:
            return Response(
                'surname is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        CoreUser.email = email
        CoreUser.language = language
        CoreUser.phone = phone
        CoreUser.firstname = firstname
        CoreUser.surname = surname
        CoreUser.save()

        Client, created = models.Client.objects.get_or_create(user__devices=Device)
        Client.user = CoreUser
        Client.save()

        result = serializers.ClientSerializer(Client).data
        result['type'] = "client"

        return Response(
            result,
            status=status.HTTP_201_CREATED
        )


class UserStatusView(APIView):

    def get(self, request, version, GUID):

        try:
            Device = models.Device.objects.get(GUID=GUID)
        except models.Device.DoesNotExist:
            return Response(
                'device with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        if not Device.active:
            return Response(
                'device with selected GUID is inactive',
                status=status.HTTP_403_FORBIDDEN
                )

        try:
            CoreUser = models.CoreUser.objects.get(devices=Device)
        except models.CoreUser.DoesNotExist:
            return Response(
                'user not found',
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            serializers.UserStatusSerializer(CoreUser.status).data,
            status=status.HTTP_200_OK
        )