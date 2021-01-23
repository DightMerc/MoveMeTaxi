from celery.decorators import task
from move_me.celery import app
from celery.utils.log import get_task_logger
import time

from core import models as models

# from feedback.emails import send_feedback_email

logger = get_task_logger(__name__)


@app.task
def search_closest_driver():

    drivers = Location.objects.filter(is_client=False)

    driver = find_closest_driver(drivers, (latitude, longitude))

    return Response(
        {
            'driver': driver
        },
        status=status.HTTP_200_OK
    )


def distance_between_two_points(location1, location2):

    return haversine(location1, location2, unit='m')


def find_closest_driver(drivers, location):
    
    min = 10000000
    target_driver = None
    logger.error(len(drivers))
    for driver_location in drivers:
        distance = distance_between_two_points(location, (float(driver_location.latitude), float(driver_location.longitude)))
        
        logger.error(distance)
        if distance < min:
            min = distance
            target_driver = driver_location.user
    
    return target_driver.GUID
