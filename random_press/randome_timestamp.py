import random


def get_random_time_part(seconds: int, part_of_time: tuple) -> int:
    is_positive = random.choice([True, False])
    part = round(seconds/random.choice(part_of_time))
    part = part if is_positive else -part
    seconds = seconds + part
    return seconds

