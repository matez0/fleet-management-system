def iter_motion(pos, speed, acc):
    """Simulates a motion with zero start and end speed from pos coordinate to the origin.

    In each iteration, the absolute speed is increased or decreased by a constant value or not changed.

    If there are more iterations left with the current speed to reach the origin
    than the iterations needed to decrease the absolute speed back to zero,
    then the absolute speed is increased.
    In the opposite case, the absolute speed is decreased.
    """
    pos += speed

    # The absolute speed needs to be changed, if abs(pos) // abs(speed) != abs(speed) // acc;
    # The speed needs to be increased, if pos < 0, decreased, if pos > 0;
    speed_change_dir = sign(abs(pos) * acc - speed * speed)

    speed = (abs(speed) + acc * speed_change_dir) * sign(-pos)

    if abs(pos) < acc and abs(speed) < acc:
        pos = speed = 0

    return pos, speed


def sign(number):
    return number and (-1 if number < 0 else 1)
