import os
import json

from typing import Optional

from model.amr import AMR
from model.time_window import TimeWindow
from model.batch import Batch
from model.task import Task
from model.kinematics import Kinematics


class DataInput:
    """
    A class for reading AMR and Batch data from files.

    Attributes:
        batch_file_path (str): The path to the batch file.
        amr_file_path (str): The path to the AMR file.
        amrs (List[AMR]): A list of AMRs read from the file.
        batches (List[Batch]): A list of Batches read from the file.
    """

    DATASETS_PATH = os.path.join(os.getcwd(), "datasets")
    BATCHES_FOLDER = "batches"
    AMRS_FOLDER = "amrs"

    def __init__(self, batch_file: str, amr_file: str):
        """
        Initializes the DataInput object with the batch and AMR file paths.

        Args:
            batch_file (str): The filename of the batch file.
            amr_file (str): The filename of the AMR file.
        """
        self.batch_file_path = os.path.join(
            DataInput.DATASETS_PATH, DataInput.BATCHES_FOLDER, batch_file)
        self.amr_file_path = os.path.join(
            DataInput.DATASETS_PATH, DataInput.AMRS_FOLDER, amr_file)

        self.amrs = None
        self.batches = None

        self.read_AMRs()
        self.read_batches()

    def read_AMRs(self):
        """
        Reads AMRs data from the file and populates the amrs list.
        """
        self.amrs = []

        id = 0
        with open(self.amr_file_path, 'r') as json_file:
            data = json.load(json_file)
            for amr_type in data['amr_types']:

                kinematics = Kinematics.create_from_dict(
                    amr_type['kinematics'])
                for i in range(amr_type['number']):

                    friendly_name = amr_type['friendly_name'] + '_' + str(id)
                    amr = AMR(id, friendly_name, kinematics)

                    self.amrs.append(amr)
                    id += 1

    def read_batches(self):
        """
        Reads Batches data from the file and populates the batches list.
        """
        self.batches = []

        with open(self.batch_file_path, 'r') as json_file:
            data = json.load(json_file)
            for batch in data['batches']:
                tasks = []
                for task in batch['tasks']:
                    start_location = (
                        task['start_location'][0], task['start_location'][1])
                    end_location = (task['end_location'][0],
                                    task['end_location'][1])
                    time_window = TimeWindow(
                        task['earliest_start'], task['latest_finish'])
                    tasks.append(
                        Task(task['id'], start_location, end_location, time_window))

                self.batches.append(Batch(batch['id'], tasks))

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for batch in self.batches:
            for task in batch.tasks:
                if task.id == task_id:
                    return task
        return None

    def get_amr_by_id(self, amr_id: int) -> Optional[Task]:
        for amr in self.amrs:
            if amr.id == amr_id:
                return amr
        return None
