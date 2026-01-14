import random
import copy


def mutate_float_vector(vec, step=0.2, prob=0.7):
    """
    Randomly perturb some elements of a float vector.
    """
    x = copy.deepcopy(vec)

    for i in range(len(x)):
        if random.random() < prob:
            x[i] += random.uniform(-step, step)

    return x


def clip_vector(vec, min_val=-10.0, max_val=10.0):
    """
    Clip values into a safe numeric range.
    """
    return [max(min(v, max_val), min_val) for v in vec]
