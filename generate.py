from itertools import product

from generator.generator import Generator


def generate_many():
    number_of_tasks = [
        100, 200, 300, 400, 500
    ]

    batch_sizes = [
        10, 20, 40,
        None  # = inf
    ]

    for t, b in product(number_of_tasks, batch_sizes):
        Generator(tasks=t, batch_size=b)


if __name__ == "__main__":

    # generate_many()

    Generator(tasks=100, batch_size=None)
