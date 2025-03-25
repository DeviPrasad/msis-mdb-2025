import numpy as np

# Calculate the inverse of the natural logarithm of M
M = 16
mL = 1 / np.log(M)
L = 8

highest_level = 0
population = [0] * 8


def get_random_level():
    global highest_level
    global population
    global mL
    # Generate a random number between 0 and 1
    r = np.random.random()
    # compute the level - exponentially decaying probability; geometric distribution.
    level = -int(np.log(r) * mL)
    # level = min(level, L)
    population[level] += 1
    if level > highest_level:
        highest_level = level


if __name__ == "__main__":
    np.random.seed()
    # Generate a few sample levels to see the distribution
    highest_level = 0
    _ = [get_random_level() for _ in range(1024 * 32)]
    print(population[: highest_level + 1])


"""
_ = [get_random_level() for _ in range(1024 * 1024 * 32)]
population = [31458174, 1965102, 122973, 7709, 443, 29, 2]

"""
