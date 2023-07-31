import math
from typing import Tuple

class Kinematics:
    """
    Provides methods for kinematic calculations.

    Attributes:
        velocity (float): The maximum velocity in meters per second.
        deceleration (float): The maximum deceleration in meters per second squared.
        acceleration (float): The maximum acceleration in meters per second squared.
        load_time (float): The load time in seconds.
        unload_time (float): The unload time in seconds.
    """

    def __init__(self, velocity: float, deceleration: float, acceleration: float, load_time: float, unload_time: float):
        """
        Initializes a Kinematics object with the given parameters.

        Args:
            velocity (float): The maximum velocity in meters per second.
            deceleration (float): The maximum deceleration in meters per second squared.
            acceleration (float): The maximum acceleration in meters per second squared.
            load_time (float): The load time in seconds.
            unload_time (float): The unload time in seconds.
        """
        self.velocity = velocity
        self.deceleration = deceleration
        self.acceleration = acceleration
        self.load_time = load_time
        self.unload_time = unload_time

    @staticmethod
    def distance(start_location: Tuple[float, float], end_location: Tuple[float, float]) -> float:
        """
        Calculate the distance between two locations.

        Args:
            start_location (Tuple[float, float]): The starting location coordinates (x, y).
            end_location (Tuple[float, float]): The ending location coordinates (x, y).

        Returns:
            float: The distance in meters.
        """
        return math.sqrt((start_location[0] - end_location[0]) ** 2 + (start_location[1] - end_location[1]) ** 2)

    def calc_time(self, start_location: Tuple[float, float], end_location: Tuple[float, float]) -> float:
        """
        Calculate the time to move from start to stop.

        Args:
            start_location (Tuple[float, float]): The starting location coordinates (x, y).
            end_location (Tuple[float, float]): The ending location coordinates (x, y).

        Returns:
            float: The time in seconds.
        """
        distance_acc = (self.velocity ** 2) / (2 * self.acceleration)
        distance_break = (self.velocity ** 2) / (2 * abs(self.deceleration))
        distance = Kinematics.distance(start_location, end_location)
        distance_threshold = distance_break + distance_acc
        time = 0

        if distance <= distance_threshold:
            time += math.sqrt((2 * distance / self.acceleration) * (abs(self.deceleration) / (self.acceleration + abs(self.deceleration))))
        else:
            time += self.velocity / self.acceleration

        if distance <= distance_threshold:
            time += math.sqrt((2 * distance / self.acceleration) * (abs(self.acceleration) / (self.acceleration + abs(self.deceleration))))
        else:
            time += self.velocity / abs(self.deceleration)
        
        if distance > distance_threshold:
            distance_const = distance - distance_acc - distance_break
            time += distance_const / self.velocity

        return time

    def __str__(self):
        """
        Returns a string representation of the Kinematics object.

        Returns:
            str: String representation of the Kinematics object.
        """
        return (
            f"Kinematics:\n"
            f"    Maximum Velocity: {self.velocity} m/s\n"
            f"    Maximum Deceleration: {self.deceleration} m/s²\n"
            f"    Maximum Acceleration: {self.acceleration} m/s²\n"
            f"    Load Time: {self.load_time} s\n"
            f"    Unload Time: {self.unload_time} s"
        )
    
    @classmethod
    def create_from_dict(cls, dictionary):
        return Kinematics(
            dictionary['velocity'],
            dictionary['deceleration'],
            dictionary['acceleration'],
            dictionary['load_time'],
            dictionary['unload_time']
        )
