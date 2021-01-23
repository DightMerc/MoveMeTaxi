from django.shortcuts import render

from rest_framework.schemas.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from core import models
import api.serializers as serializers

import json
import random

import os
from twilio.rest import Client as TwilioClient

import logging
logger = logging.getLogger(__name__)


class DeviceView(APIView):

    def get(self, request, version):
        device_list = models.Device.objects.all()
        return Response(
            serializers.DeviceSerializer(device_list, many=True).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, version):

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set',
                status=status.HTTP_400_BAD_REQUEST
                )

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

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
        sms_phone_number = os.environ.get('TWILIO_PHONE_NUMBER', '')

        client = TwilioClient(account_sid, auth_token)

        try:
            message = client.messages.create(
                body=f'Your verification code in MoveMe: {verification_code}',
                from_=sms_phone_number,
                to=f'+{phone}'
            )
        except Exception as e:
            logger.error(e)

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

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set',
                status=status.HTTP_400_BAD_REQUEST
                )

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

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set',
                status=status.HTTP_400_BAD_REQUEST
                )

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


class RideView(APIView):

    def post(self, request, version, GUID):

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set',
                status=status.HTTP_400_BAD_REQUEST
                )

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
            from_address = data['from']
        except Exception as e:
            return Response(
                'from is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            to_address = data['to']
        except Exception as e:
            return Response(
                'to is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            client = models.Client.objects.get(user__devices__GUID=GUID)
        except Exception as e:
            return Response(
                'client wit selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        try:
            fare_policy = str(data['fare_policy'])
        except Exception as e:
            return Response(
                'fare_policy is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            payment_type = str(data['payment_type'])
        except Exception as e:
            return Response(
                'payment_type is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        # TODO change to GUID

        # try:
        #     fare_policy = models.FarePolicy.objects.get(GUID=fare_policy)
        # except Exception as e:
        #     return Response(
        #         'fare_policy with selected GUID not found',
        #         status=status.HTTP_404_NOT_FOUND
        #         )

        try:
            fare_policy = models.FarePolicy.objects.get(title=fare_policy)
        except Exception as e:
            return Response(
                'fare_policy with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        try:
            payment_type = models.PaymentType.objects.get(GUID=payment_type)
        except Exception as e:
            return Response(
                'payment_type with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        address = from_address
        newAddress = models.Address()
        try:
            newAddress.title = address['title']
        except Exception as e:
            return Response(
                    'title not set: ' + str(address),
                    status=status.HTTP_400_BAD_REQUEST
                    )

        try:
            newAddress.latitude = address['latitude']
        except Exception as e:
            return Response(
                    'latitude not set: ' + str(address),
                    status=status.HTTP_400_BAD_REQUEST
                    )

        try:
            newAddress.longitude = address['longitude']
        except Exception as e:
            return Response(
                    'longitude not set: ' + str(address),
                    status=status.HTTP_400_BAD_REQUEST
                    )

        try:
            newAddress.entrance = address['entrance']
        except Exception as e:
            newAddress.entrance = ''

        try:
            newAddress.comment = address['comment']
        except Exception as e:
            newAddress.comment = ''

        newAddress.save()

        NewRide = models.Ride()
        NewRide.client = client
        NewRide.start_point = newAddress
        NewRide.fare_policy = fare_policy
        NewRide.payment_type = payment_type
        NewRide.status = models.RideStatus.objects.first()
        NewRide.save()

        for address in to_address:

            newAddress = models.Address()
            try:
                newAddress.title = address['title']
            except Exception as e:
                return Response(
                        'title not set: ' + str(address),
                        status=status.HTTP_400_BAD_REQUEST
                        )

            try:
                newAddress.latitude = address['latitude']
            except Exception as e:
                return Response(
                        'latitude not set: ' + str(address),
                        status=status.HTTP_400_BAD_REQUEST
                        )

            try:
                newAddress.longitude = address['longitude']
            except Exception as e:
                return Response(
                        'longitude not set: ' + str(address),
                        status=status.HTTP_400_BAD_REQUEST
                        )

            try:
                newAddress.house = address['house']
            except Exception as e:
                newAddress.house = ''

            try:
                newAddress.comment = address['comment']
            except Exception as e:
                newAddress.comment = ''

            newAddress.save()

            NewRide.end_point.add(newAddress)

        return Response(
            serializers.RideSerializer(NewRide).data,
            status=status.HTTP_201_CREATED
        )


class RideInfo(APIView):

    def get(self, request, version, GUID, RIDE_GUID):

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
            ride = models.Ride.objects.get(GUID=RIDE_GUID)
        except models.Ride.DoesNotExist:
            return Response(
                'ride with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializers.RideSerializer(ride).data,
            status=status.HTTP_200_OK
        )


class RideStatus(APIView):

    def get(self, request, version, GUID, RIDE_GUID):

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
            ride = models.Ride.objects.get(GUID=RIDE_GUID)
        except models.Ride.DoesNotExist:
            return Response(
                'ride with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializers.RideStatusSerializer(ride.status).data,
            status=status.HTTP_200_OK
        )


class RideReview(APIView):

    def get(self, request, version, GUID, RIDE_GUID):

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
            ride = models.Ride.objects.get(GUID=RIDE_GUID)
        except models.Ride.DoesNotExist:
            return Response(
                'ride with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializers.ReviewSerializer(ride.review).data,
            status=status.HTTP_200_OK
        )

    def post(self, request, version, GUID, RIDE_GUID):

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set',
                status=status.HTTP_400_BAD_REQUEST
                )

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
            ride = models.Ride.objects.get(GUID=RIDE_GUID)
        except models.Ride.DoesNotExist:
            return Response(
                'ride with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        newReview = models.Review()

        try:
            newReview.stars = int(data['stars'])
        except Exception as e:
            newReview.stars = 0

        try:
            newReview.comment = int(data['comment'])
        except Exception as e:
            newReview.comment = ''

        try:
            newReview.reason = int(data['reason'])
        except Exception as e:
            newReview.reason = ''

        newReview.save()
        ride.review = newReview.save()

        return Response(
            serializers.ReviewSerializer(newReview).data,
            status=status.HTTP_201_CREATED
        )


class FarePolicyView(APIView):

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

        fare_policies = models.FarePolicy.objects.filter(active=True)

        result = []
        for policy in fare_policies:
            if policy.temp:
                if policy.closes_at > datetime.now():
                    result.append(policy)
                else:
                    policy.active = False
            else:
                result.append(policy)

        return Response(
            serializers.FarePolicySerizlier(result, many=True).data,
            status=status.HTTP_200_OK
        )


class RideAccept(APIView):

    def get(self, request, version, GUID, RIDE_GUID):

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
            ride = models.Ride.objects.get(GUID=RIDE_GUID)
        except models.Device.DoesNotExist:
            return Response(
                'ride with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        try:
            CoreUser = models.CoreUser.objects.get(devices=Device)
        except models.CoreUser.DoesNotExist:
            return Response(
                'user not found',
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            user = models.Driver.objects.get(user=CoreUser)
        except models.Driver.DoesNotExist:
            return Response(
                'driver not found',
                status=status.HTTP_404_NOT_FOUND
            )

        if ride.driver is None:

            ride.driver = user
            ride.save()

            return Response(
                'OK',
                status=status.HTTP_200_OK
            )

        else:

            return Response(
                f'ride has been already accepted by another driver: {ride.driver.user.GUID}',
                status=status.HTTP_404_NOT_FOUND
            )
