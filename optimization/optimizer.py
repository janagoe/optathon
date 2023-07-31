from abc import ABC, abstractmethod

from model.batch import Batch

from framework.data_input import DataInput
from framework.scheduling_output import SchedulingOutput


class Optimizer(ABC):

    def run(self, data_input: DataInput) -> SchedulingOutput:
        self.data_input = data_input
        self.scheduling_output = SchedulingOutput(self.data_input)

        self.init_optimization()

        for batch in data_input.batches:
            self.process_batch(batch)

        return self.scheduling_output

    @abstractmethod
    def init_optimization(self) -> None:
        pass

    @abstractmethod
    def process_batch(self, batch: Batch) -> None:
        pass
