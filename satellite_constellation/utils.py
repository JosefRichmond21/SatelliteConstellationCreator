"""

"""
import math
import numpy as np


def mod(x, y):
    """
    Mappable modulo function
    :param x: First number
    :param y: Second number
    :return: x % y
    """
    return [a % b for a, b in zip(x, y)]


heavenly_body_radius = {  # [km]
    "earth": 6371,
    "luna": 1737,
    "mars": 3390,
    "venus": 6052,
    "mercury": 2440,
    "sol": 695700,
    "jupiter": 69911,
    "saturn": 58232,
    "uranus": 25362,
    "neptune": 24622,
    "pluto": 1188,
}

heavenly_body_mass = {  # [kg]
    "earth": 5.972 * 10 ** 24,
    "luna": 73.46 * 10 ** 21,
    "mars": 641.71 * 10 ** 21,
    "venus": 4867.5 * 10 ** 21,
    "mercury": 330.11 * 10 ** 21,
    "sol": 1.9885 * 10 ** 30,
    "jupiter": 1.8982 * 10 ** 27,
    "saturn": 5.6834 * 10 ** 26,
    "uranus": 8.6810 * 10 ** 25,
    "neptune": 1.02413 * 10 ** 26,
    "pluto": 13.03 * 10 ** 21,
}

heavenly_body_period = {  # [days]
    "earth": 1,
    "luna": 27.321661,
    "mars": 1.02595675,
    "venus": 243.0187,
    "mercury": 58.6462,
    "sol": 25.379995,
    "jupiter": 0.41007,
    "saturn": 0.426,
    "uranus": 0.71833,
    "neptune": 0.67125,
    "pluto": 6.38718,
}

constants = {
    "G": 6.67408 * 10 ** (-11),  # Gravitational constant [m^3 kg^-1 s^-2]
    "wE": 7.2921159 * 10 ** (-5),  # Earth angular velocity [rad/s]
    "J2E": 10826269 * 10 ** (-3),  # Earth J2 constant
}


def proper_round(num, dec=0):  # Add exception check for no decimal point found

    num = str(num)[:str(num).index('.') + dec + 2]
    if num[-1] >= '5':
        return float(num[:-2 - (not dec)] + str(int(num[-2 - (not dec)]) + 1))
    return float(num[:-1])


def polar2cart(r, phi, theta):
    return [
        r * math.sin(phi) * math.cos(theta),
        r * math.sin(theta) * math.sin(phi),
        r * math.cos(phi)
    ]


def rotate(vec, ang, ax='x', rpy=[0, 0, 0], basis=None):
    if ax == 'x':
        r_x = np.array([[1, 0, 0],
                        [0, math.cos(ang), -1 * math.sin(ang)],
                        [0, math.sin(ang), math.cos(ang)]])
        return np.matmul(r_x, vec)
    elif ax == 'y':
        r_y = np.array([[math.cos(ang), 0, math.sin(ang)],
                        [0, 1, 0],
                        [-math.sin(ang), 0, math.cos(ang)]])
        return np.matmul(r_y, vec)
    elif ax == 'z':
        r_z = np.array([[math.cos(ang), -math.sin(ang), 0],
                        [math.sin(ang), math.cos(ang), 0],
                        [0, 0, 1]])
        return np.matmul(r_z, vec)
    elif ax == 'c':
        ang_yaw, ang_pitch, ang_roll = rpy[2], rpy[1], rpy[0]
        ang_yaw *= math.pi / 180
        ang_pitch *= math.pi / 180
        ang_roll *= math.pi / 180
        r_yaw = np.array([[1, 0, 0],
                          [0, math.cos(ang_yaw), -1 * math.sin(ang_yaw)],
                          [0, math.sin(ang_yaw), math.cos(ang_yaw)]])
        r_pitch = np.array([[math.cos(ang_pitch), 0, math.sin(ang_pitch)],
                            [0, 1, 0],
                            [-math.sin(ang_pitch), 0, math.cos(ang_pitch)]])
        r_roll = np.array([[math.cos(ang_roll), 0, math.sin(ang_roll)],
                           [0, 1, 0],
                           [-math.sin(ang_roll), 0, math.cos(ang_roll)]])
        r_c = np.matmul(r_yaw, r_pitch)
        r_c = np.matmul(r_c, r_roll)
        r_c = np.matmul(r_c, vec)
        return r_c
    elif ax == "custom":
        ux = basis[0]
        uy = basis[1]
        uz = basis[2]
        a = (1 - math.cos(ang))
        R = np.array([
            [math.cos(ang) + math.pow(ux, 2) * a, ux * uy * a - uz * math.sin(ang), ux * uz * a + uy * math.sin(ang)],
            [ux * uy * a + uz * math.sin(ang), math.cos(ang) + math.pow(uy, 2) * a, uy * uz * a - ux * math.sin(ang)],
            [uz * ux * a - uy * math.sin(ang), uz * uy * a + ux * math.sin(ang), math.cos(ang) + math.pow(uz, 2) * a]])
        return np.matmul(R, vec)


def sphere_intercept(P1, P2, R):
    x1 = P1[0]
    x2 = P2[0]
    y1 = P1[1]
    y2 = P2[1]
    z1 = P1[2]
    z2 = P2[2]

    a = math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2)
    b = 2 * (x1 * (x2 - x1) + y1 * (y2 - y1) + z1 * (z2 - z1))
    c = math.pow(x1, 2) + math.pow(y1, 2) + math.pow(z1, 2) - math.pow(R, 2)

    determinant = math.pow(b, 2) - 4 * a * c
    if determinant < 0:
        return False
    elif determinant == 0:
        return True
    else:
        return True
