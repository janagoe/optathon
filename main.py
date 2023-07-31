import time
import os
from framework.data_input import DataInput
from framework.evaluation import Evaluation

from optimization.round_robin import RoundRobin


def execute(batch_file: str, amr_file: str, OptimizerImpl) -> Evaluation:

    data_input = DataInput(batch_file, amr_file)

    # --------------------------

    start_time = time.time()

    optimizer = OptimizerImpl()
    scheduling_output = optimizer.run(data_input)

    end_time = time.time()

    # --------------------------

    evaluation = Evaluation(data_input)
    evaluation.set_execution_time(end_time - start_time)
    evaluation.evaluate(scheduling_output)

    return evaluation


if __name__ == "__main__":

    batch_path = os.path.join(os.getcwd(), 'datasets', 'batches')
    for batch_file in sorted(os.listdir(batch_path)):

        evaluation = execute(batch_file, 'amrs_15.json', RoundRobin)

        print("\n\nFile ", batch_file)
        print(evaluation)
