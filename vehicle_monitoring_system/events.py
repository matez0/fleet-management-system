import logging

from if_gs_vms import GpsMessage, ROUTING_KEY_GPS, TIME_DIFF, ACC
from if_vms_fms import PenaltyMessage, ROUTING_KEY_PENALTY
from messaging import Callback, send_message, start_consumer

logger = logging.getLogger('django')

SPEED_LIMIT1 = 60
SPEED_LIMIT2 = 80
SPEED_LIMIT3 = 100


def start_consuming_gps_events():
    start_consumer(ROUTING_KEY_GPS, process_gps_event)


@Callback(GpsMessage)
def process_gps_event(message: GpsMessage, header):
    logger.info('Incoming message; message=%s', message)

    penalty_points = calculate_penalty(message.speed)

    if penalty_points:
        send_message(ROUTING_KEY_PENALTY, PenaltyMessage(driverId=message.driverId, points=penalty_points))


def calculate_penalty(speed):
    penalty_points = 0
    for speed_limit, penalty_unit in [(100, 5), (80, 2), (60, 1)]:
        if speed > speed_limit:
            penalty_points += penalty_unit * (speed - speed_limit)
            speed %= speed_limit

    return penalty_points
