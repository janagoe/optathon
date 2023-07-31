from typing import Tuple
from model.time_window import TimeWindow

class Task:
    """
    Represents a task with specific locations and a time window.

    Attributes:
        id (int): The task identifier.
        start_location (Tuple[float, float]): The start location coordinates (latitude, longitude).
        end_location (Tuple[float, float]): The end location coordinates (latitude, longitude).
        time_window (TimeWindow): The time window in which the task must be executed.
    """

    def __init__(self, task_id: int, start_location: Tuple[float, float], end_location: Tuple[float, float], time_window: TimeWindow):
        """
        Initializes a Task object.

        Args:
            task_id (int): The task identifier.
            start_location (Tuple[float, float]): The start location coordinates (latitude, longitude).
            end_location (Tuple[float, float]): The end location coordinates (latitude, longitude).
            time_window (TimeWindow): The time window in which the task must be executed.
        """
        self.id = task_id
        self.start_location = start_location
        self.end_location = end_location
        self.time_window = time_window

    def __str__(self):
        """
        Returns a string representation of the Task object.

        Returns:
            str: String representation of the Task object.
        """
        task_str = f"Task {self.id}:\n"
        task_str += f"    Start Location: {self.start_location}\n"
        task_str += f"    End Location: {self.end_location}\n"
        task_str += f"    Time Window: {self.time_window}"

        return task_str
    
    def __eq__(self, other):
        """
        Comparison method to check if two Task objects are equal based on their id.

        Args:
            other (Task): Another Task object to compare.

        Returns:
            bool: True if the Task objects have the same id, False otherwise.
        """
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self):
        """
        Hash method based on the Task id.

        Returns:
            int: The hash value of the Task object based on its id.
        """
        return hash(self.id)
