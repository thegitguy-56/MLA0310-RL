import numpy as np

# ---------- USER INPUT ----------
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

grid = np.zeros((rows, cols))

print("\nEnter obstacle locations:")
obs = int(input("Number of obstacles: "))
for _ in range(obs):
    r, c = map(int, input("Obstacle (row col): ").split())
    grid[r][c] = -999  # obstacle marker

print("\nEnter delivery points:")
goals = int(input("Number of delivery points: "))
delivery_points = []
for _ in range(goals):
    r, c = map(int, input("Delivery point (row col): ").split())
    delivery_points.append((r, c))

gamma = float(input("\nEnter discount factor (e.g., 0.9): "))

# ---------- ACTIONS ----------
actions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

# ---------- INITIALIZE ----------
V = np.zeros((rows, cols))
policy = np.full((rows, cols), "RIGHT", dtype=object)

def valid(r, c):
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] != -999

# ---------- POLICY EVALUATION ----------
def policy_evaluation():
    while True:
        delta = 0
        for r in range(rows):
            for c in range(cols):
                if (r, c) in delivery_points or grid[r][c] == -999:
                    continue

                action = policy[r][c]
                dr, dc = actions[action]
                nr, nc = r + dr, c + dc

                if valid(nr, nc):
                    reward = -1
                    v_new = reward + gamma * V[nr][nc]
                else:
                    v_new = V[r][c]

                delta = max(delta, abs(V[r][c] - v_new))
                V[r][c] = v_new

        if delta < 0.01:
            break

# ---------- POLICY IMPROVEMENT ----------
def policy_improvement():
    stable = True
    for r in range(rows):
        for c in range(cols):
            if (r, c) in delivery_points or grid[r][c] == -999:
                continue

            old_action = policy[r][c]
            best_value = float("-inf")
            best_action = old_action

            for a, (dr, dc) in actions.items():
                nr, nc = r + dr, c + dc
                if valid(nr, nc):
                    value = -1 + gamma * V[nr][nc]
                    if value > best_value:
                        best_value = value
                        best_action = a

            policy[r][c] = best_action
            if old_action != best_action:
                stable = False

    return stable

# ---------- POLICY ITERATION ----------
while True:
    policy_evaluation()
    if policy_improvement():
        break

# ---------- OUTPUT ----------
print("\nOptimal Value Function:")
for row in V:
    print(["{:.2f}".format(v) for v in row])

print("\nOptimal Policy:")
for r in range(rows):
    row_policy = []
    for c in range(cols):
        if (r, c) in delivery_points:
            row_policy.append("GOAL")
        elif grid[r][c] == -999:
            row_policy.append("XXXX")
        else:
            row_policy.append(policy[r][c])
    print(row_policy)
