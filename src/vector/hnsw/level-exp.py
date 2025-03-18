import numpy as np

level_gt_3 = 0


def get_random_level(mL):
    global level_gt_3
    # Generate a random number between 0 and 1
    r = np.random.rand()
    # Compute the level using the exponential distribution property
    level = int(-np.log(r) * mL)
    if level > 3:
        level_gt_3 += 1
        print(f"{level_gt_3} r = {r}, level = {level}")
    return level


# Define the maximum number of neighbors at level 0 (M)
M = 16  # This is an example value; in practice, M might be set differently.
# Calculate mL as the inverse of the natural logarithm of M
mL = 1 / np.log(M)

# Generate a few sample levels to see the distribution
level_gt_2 = 0
levels = [get_random_level(mL) for _ in range(1024 * 1024)]
print("Sample levels:", [level for level in levels if level > 3])
