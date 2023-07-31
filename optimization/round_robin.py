from optimization.optimizer import Optimizer

from model.batch import Batch


class RoundRobin(Optimizer):

    def init_optimization(self) -> None:
        raise NotImplementedError()

    def process_batch(self, batch: Batch) -> None:
        raise NotImplementedError()
