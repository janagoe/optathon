from typing import Tuple

from collections import defaultdict
from model.kinematics import Kinematics


class Assignment:

    def __init__(self, amr_id, task_id, start_time, duration, empty_travel_distance, lateness):
        self.amr_id = amr_id
        self.task_id = task_id
        self.start_time = start_time

        # helpers
        self.duration = duration
        self.empty_travel_distance = empty_travel_distance
        self.lateness = lateness


class SchedulingOutput:
    """
    Represents the scheduling output of tasks assigned to AMRs at specific starting times.

    Attributes:
        task_assignments (List[Tuple[int, int, float]]): List of task assignments for each AMR.
            Each tuple contains (task_id, amr_id, assigned_time).
    """

    def __init__(self, data_input):
        self.data_intput = data_input
        self.assignments = defaultdict(list)

    def add_assignment(self, amr_id: int, task_id: int, start_time=None):
        if start_time is None:

            if len(self.assignments[amr_id]) == 0:
                start_time = 0
            else:
                last_assignment = self.assignments[amr_id][-1]
                assert (last_assignment.duration is not None)

                start_time = last_assignment.start_time + last_assignment.duration

        duration, empty_travel_distance, lateness = self._calc_assignment_metrics(
            amr_id, task_id, start_time)

        assert (duration is not None)
        assert (empty_travel_distance is not None)
        assert (lateness is not None)

        self.assignments[amr_id].append(
            Assignment(amr_id, task_id, start_time, duration, empty_travel_distance, lateness))

    def _calc_assignment_metrics(self, amr_id, task_id, start_time) -> Tuple[float, float]:

        kinematics = self.data_intput.get_amr_by_id(amr_id).kinematics
        task = self.data_intput.get_task_by_id(task_id)

        if len(self.assignments[amr_id]) == 0:
            last_location = (0.0, 0.0)
        else:
            previous_task_id = self.assignments[amr_id][-1].task_id
            previous_task = self.data_intput.get_task_by_id(previous_task_id)

            last_location = previous_task.end_location

        empty_travel_duration = kinematics.calc_time(
            last_location, task.start_location)

        empty_travel_distance = Kinematics.distance(
            last_location, task.start_location)

        execution_duration = kinematics.calc_time(
            task.start_location, task.end_location)

        task_end_time = start_time + empty_travel_duration + execution_duration
        lateness = max(0, task_end_time - task.time_window.latest_finish)

        return empty_travel_duration + execution_duration, empty_travel_distance, lateness
