x = 130

v = 0

DV = 1


def sign(number):
    return number and (-1 if number < 0 else 1)


def iter_motion(x, v):
    """Simulates a motion with zero start and end speed from x coordinate to the origin.

    In each iteration, the absolute speed is increased or decreased by a constant value or not changed.

    If there are more iterations left with the current speed to reach the origin
    than the iterations needed to decrease the absolute speed back to zero,
    then the absolute speed is increased.
    In the opposite case, the absolute speed is decreased.
    """
    x += v

    # The absolute speed needs to be changed, if abs(x) // abs(v) != abs(v) // DV;
    # The speed needs to be increased, if x < 0, decreased, if x > 0;
    speed_change_dir = sign((v * v - abs(x) * DV) * x)

    v += DV * speed_change_dir

    return x, v


while x != 0:
    print(x, v)

    x, v = iter_motion(x, v)
