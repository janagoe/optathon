from model.task import Task
from typing import List

class Batch:
    """
    Represents a batch of tasks with a common spawn time.
    The optimizer is able to see all tasks from a batch at once. 

    Attributes:
        id (int): The unique identifier for the batch.
        spawn_time (float): The spawn time in seconds for all tasks in the batch.
        tasks (List[Task]): The list of tasks in the batch.
    """

    def __init__(self, batch_id: int, tasks: List[Task]):
        """
        Initializes a Batch object with the given spawn time.

        Args:
            batch_id (int): The unique identifier for the batch.
            spawn_time (float): The spawn time in seconds for all tasks in the batch.
        """
        self.id = batch_id
        self.tasks = tasks

    def __str__(self):
        """
        Returns a string representation of the Batch object.

        Returns:
            str: String representation of the Batch object.
        """
        batch_str = f"Batch {self.id}:\n"

        for task in self.tasks:
            task_str = f"    Task {task.id}:\n"
            task_str += f"        Start Location: {task.start_location}\n"
            task_str += f"        End Location: {task.end_location}\n"
            task_str += f"        Time Window: {task.time_window}\n"
            batch_str += task_str

        return batch_str
