from typing import Optional

class TimeWindowException(Exception):
    pass


class TimeWindow:
    """
    Represents a time window with optional spawn time and duration.

    Attributes:
        earliest_start (float): The earliest start time in seconds.
        latest_finish (float): The latest finish time in seconds.
        duration (Optional[float]): The duration of the time window in seconds (if set).
        spawn_time_set (bool): Indicates whether the spawn time has been set.
    """

    def __init__(self, earliest_start: float, latest_finish: float, spawn_time: Optional[float] = None, duration: Optional[float] = None):
        """
        Initializes a TimeWindow object.

        Args:
            earliest_start (float): The earliest start time in seconds.
            latest_finish (float): The latest finish time in seconds.
            spawn_time (Optional[float]): The spawn time in seconds (default: None).
            duration (Optional[float]): The duration of the time window in seconds (default: None).
        """
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.duration = None
        self.spawn_time_set = False

        if spawn_time is not None:
            self.set_spawn_time(spawn_time)

        if duration is not None:
            self.set_duration(duration)

    def set_duration(self, duration: float):
        """
        Sets the duration of the time window, meaning how long an AMR requires for the execution. 

        Args:
            duration (float): The duration of the time window in seconds.
        """
        self.duration = duration
        self.earliest_finish = self.earliest_start + duration
        self.latest_start = self.latest_finish - duration

    def set_spawn_time(self, spawn_time: float):
        """
        Sets the spawn time for the time window.

        Args:
            spawn_time (float): The spawn time in seconds.
        
        Raises:
            TimeWindowException: If the spawn time has already been set.
        """
        if self.spawn_time_set:
            raise TimeWindowException("Spawn time has already been set.")

        self.earliest_start += spawn_time
        self.latest_finish += spawn_time
        self.spawn_time_set = True

        if hasattr(self, "earliest_finish"):
            self.earliest_finish += spawn_time
        if hasattr(self, "latest_start"):
            self.latest_start += spawn_time

    def __str__(self):
        """
        Returns a string representation of the TimeWindow object.

        Returns:
            str: String representation of the TimeWindow object.
        """
        time_window_str = f"TimeWindow: [{self.earliest_start} s ; {self.latest_finish} s]"

        if hasattr(self, 'earliest_finish'):
            time_window_str += f" (Earliest Finish: {self.earliest_finish} s)"

        if hasattr(self, 'latest_start'):
            time_window_str += f" (Latest Start: {self.latest_start} s)"

        if self.duration is not None:
            time_window_str += f" (Duration: {self.duration} s)"

        return time_window_str
