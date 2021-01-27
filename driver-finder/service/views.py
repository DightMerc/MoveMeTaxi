from django.shortcuts import render

from rest_framework.schemas.views import APIView
from rest_framework.response import Response
from rest_framework import status

from haversine import haversine

from math import asin, cos, radians, sin, sqrt

from core import models
from service.models import Location, Mention

from pyfcm import FCMNotification

import json
import os
import random

import time

import logging
from finder.celery import app
logger = logging.getLogger(__name__)

push_service = FCMNotification(api_key=os.environ.get("FCM_TOKEN", "empty_key"))


class FindClosestDriver(APIView):

    def post(self, request, version):

        try:
            data = json.loads(request.body)
        except Exception as e:
            return Response(
                'request body not set: ' + str(e),
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
            ride = str(data['ride'])
        except Exception as e:
            return Response(
                'ride is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        if not models.Ride.objects.filter(GUID=ride).exists():
            return Response(
                'ride with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        try:
            fare_policy = str(data['fare_policy'])
        except Exception as e:
            return Response(
                'fare_policy is not set',
                status=status.HTTP_400_BAD_REQUEST
                )

        if not models.FarePolicy.objects.filter(GUID=fare_policy).exists():
            return Response(
                'fare_policy with selected GUID not found',
                status=status.HTTP_404_NOT_FOUND
                )

        try:
            latitude = float(location['latitude'])
            longitude = float(location['longitude'])
        except Exception as e:
            return Response(
                'location format is wrong',
                status=status.HTTP_400_BAD_REQUEST
                )

        # drivers = Location.objects.filter(is_client=False)

        radius = 1000

        find_closest_driver.delay(
            (latitude, longitude),
            radius,
            ride,
            fare_policy
            )

        return Response(
            {
                'driver': 'ok'
            },
            status=status.HTTP_200_OK
        )


def distance_between_two_points(location1, location2):

    return haversine(location1, location2, unit='m')


def set_ride_driver(driver, ride):

    driver = models.CoreUser.objects.get(GUID=driver)
    ride = models.Ride.objects.get(GUID=ride)

    ride.driver = driver
    ride.save()


@app.task
def find_closest_driver(location, radius, rideGUID, fare_policy):

    drivers = Location.objects.filter(is_client=False)

    min = 10000000
    radius_incrementation = 100
    radius_max = 2600
    pause = 1
    driver_answer_pause = 5
    target_driver = None

    valid_drivers = []

    counter = 0

    while True:

        newDriverDetected = False
        ride = models.Ride.objects.get(GUID=rideGUID)

        if ride.status.title == 'looking_for_driver' and ride.driver is None:

            counter += 1

            logger.error(f'///\ncycle: {counter}\nride: {ride.GUID}\ndriver: {ride.driver}\nradius: {radius}\nmin distance: {min}\nvalid drivers: {len(valid_drivers)}')

            for driver_location in drivers:

                if driver_location.user.status.title == 'online':

                    driver = models.Driver.objects.get(user__GUID=driver_location.user.GUID)

                    if driver.fare_policy.GUID == fare_policy:

                        distance = distance_between_two_points(location, (float(driver_location.latitude), float(driver_location.longitude)))

                        if radius > distance:

                            if driver_location.user.GUID not in valid_drivers:

                                valid_drivers.append(driver_location.user.GUID)
                                newDriverDetected = True

                                markDriverAsValid(driver_location.user.GUID, ride)
                                # sendNotificationToDriver(driver_location.user)

                            if distance < min:

                                min = distance
                                target_driver = driver_location.user

            if radius == radius_max - radius_incrementation:
                break
            else:
                radius += radius_incrementation

            # TODO check disabling algorythm
            
            # if counter == 15:
            #     break

            if newDriverDetected:
                logger.error(f'waiting for driver answer: {driver_answer_pause}')
                time.sleep(driver_answer_pause)

            else:
                time.sleep(pause)
        else:

            return ride.driver.user.GUID


def markDriverAsValid(user, ride):

    mention = Mention.objects.get(user__GUID=user)
    mention.active = True
    mention.ride = ride
    mention.save()


def markDriverAsInValid(user, ride):

    mention = Mention.objects.get(user__GUID=user)
    mention.active = False
    mention.ride = ride
    mention.save()


def sendNotificationToDriver(user):

    device = user.devices.filter(active=True).first()

    registration_id = device.notificationID
    message_title = 'New Ride!'
    message_body = 'New ride request!'

    result = push_service.notify_single_device(
        registration_id=registration_id,
        message_title=message_title,
        message_body=message_body
        )

    return result
