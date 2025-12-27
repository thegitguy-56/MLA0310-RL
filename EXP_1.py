import random

GRID_SIZE = 5

# Grid definition
# 0 = empty, 1 = dirt, -1 = obstacle
grid = [
    [0, 0, 1, 0, 0],
    [0, -1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 0, -1, 0, 0],
    [0, 0, 0, 1, 0]
]

actions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

def is_valid(r, c):
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

def greedy_policy(pos):
    r, c = pos
    best_action = None
    best_reward = -999

    for action, (dr, dc) in actions.items():
        nr, nc = r + dr, c + dc
        if is_valid(nr, nc):
            reward = grid[nr][nc]
            if reward > best_reward:
                best_reward = reward
                best_action = action

    return best_action

def random_policy():
    return random.choice(list(actions.keys()))

def simulate(policy_type):
    r, c = 0, 0
    total_reward = 0
    steps = 0
    dirt_left = sum(row.count(1) for row in grid)

    print("\nStarting Simulation...\n")

    while dirt_left > 0 and steps < 50:
        if policy_type == "1":
            action = random_policy()
        else:
            action = greedy_policy((r, c))

        dr, dc = actions[action]
        nr, nc = r + dr, c + dc

        if is_valid(nr, nc):
            r, c = nr, nc
            reward = grid[r][c]
            total_reward += reward

            if grid[r][c] == 1:
                grid[r][c] = 0
                dirt_left -= 1

        steps += 1
        print(f"Step {steps}: Action={action}, Position=({r},{c}), Reward={total_reward}")

    print("\nSimulation Ended")
    print("Total Reward:", total_reward)
    print("Steps Taken:", steps)

# ------------------ USER INPUT ------------------

print("Choose Policy:")
print("1. Random Policy")
print("2. Greedy Policy")

choice = input("Enter choice (1 or 2): ")
simulate(choice)
