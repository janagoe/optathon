from framework.data_input import DataInput
from framework.scheduling_output import SchedulingOutput


class Evaluation:
    """
    Class for evaluating the scheduling output generated by optimization algorithms.
    """

    def __init__(self, data_input: DataInput):
        """
        Initializes the Evaluation object with the given DataInput.

        Args:
            data_input (DataInput): The data input for the evaluation.
        """
        self.data_input = data_input
        self.total_makespan = None
        self.total_distance = None
        self.total_time = None
        self.lateness = None
        self.execution_time = None

    def set_execution_time(self, execution_time: float):
        """
        Set the execution time of the optimization algorithm.

        Args:
            execution_time (float): The execution time in seconds.
        """
        self.execution_time = execution_time

    def __str__(self):
        """
        Returns a string representation of the Evaluation object.

        Returns:
            str: String representation of the Evaluation object.
        """
        evaluation_str = "Evaluation Results:\n"
        evaluation_str += f"    Total Makespan: {self.total_makespan:.2f} seconds\n"
        evaluation_str += f"    Total Empty Travel Distance: {self.total_distance:.2f} meters\n"
        evaluation_str += f"    Total Execution Time: {self.total_time:.2f} seconds\n"
        evaluation_str += f"    Lateness: {self.lateness}\n"
        evaluation_str += f"    Execution Time: {self.execution_time:.5f} seconds\n"
        return evaluation_str

    def evaluate(self, scheduling_output: SchedulingOutput):
        self.total_makespan = 0
        self.total_distance = 0
        self.total_time = 0
        self.lateness = 0

        for amr_id, assignments in scheduling_output.assignments.items():

            max_end_time = max(
                map(lambda ass: ass.start_time + ass.duration, assignments))
            self.total_makespan = max(max_end_time, self.total_makespan)

            self.total_distance += sum(map(
                lambda ass: ass.empty_travel_distance,
                assignments))

            self.total_time += sum(map(
                lambda ass: ass.duration,
                assignments))

            self.lateness += sum(map(
                lambda ass: ass.lateness,
                assignments))