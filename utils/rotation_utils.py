import math

import numpy as np


def axis_to_rpy(axis):
    x, y, z = axis

    yaw = math.atan2(y, x)
    pitch = math.atan2(-z, np.sqrt(x * x + y * y))
    roll = 0.0

    return roll, pitch, yaw
