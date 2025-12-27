import numpy as np

# ---------- USER INPUT ----------
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

gamma = float(input("Enter discount factor (e.g., 0.9): "))
theta = 0.01

# Grid initialization
grid = np.zeros((rows, cols))

print("\nEnter obstacle locations:")
obs = int(input("Number of obstacles: "))
for _ in range(obs):
    r, c = map(int, input("Obstacle (row col): ").split())
    grid[r][c] = -999  # obstacle marker

print("\nEnter pickup locations:")
pickups = int(input("Number of pickup points: "))
pickup_points = []
for _ in range(pickups):
    r, c = map(int, input("Pickup point (row col): ").split())
    pickup_points.append((r, c))

# ---------- ACTIONS ----------
actions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

# ---------- INITIALIZE ----------
V = np.zeros((rows, cols))
policy = np.full((rows, cols), "", dtype=object)

def valid(r, c):
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] != -999

# ---------- VALUE ITERATION ----------
while True:
    delta = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) in pickup_points or grid[r][c] == -999:
                continue

            v = V[r][c]
            max_value = float("-inf")

            for action, (dr, dc) in actions.items():
                nr, nc = r + dr, c + dc
                if valid(nr, nc):
                    reward = 10 if (nr, nc) in pickup_points else -1
                    value = reward + gamma * V[nr][nc]
                    max_value = max(max_value, value)

            V[r][c] = max_value
            delta = max(delta, abs(v - V[r][c]))

    if delta < theta:
        break

# ---------- POLICY EXTRACTION ----------
for r in range(rows):
    for c in range(cols):
        if (r, c) in pickup_points:
            policy[r][c] = "PICK"
            continue
        if grid[r][c] == -999:
            policy[r][c] = "XXXX"
            continue

        best_action = None
        best_value = float("-inf")

        for action, (dr, dc) in actions.items():
            nr, nc = r + dr, c + dc
            if valid(nr, nc):
                reward = 10 if (nr, nc) in pickup_points else -1
                value = reward + gamma * V[nr][nc]
                if value > best_value:
                    best_value = value
                    best_action = action

        policy[r][c] = best_action

# ---------- OUTPUT ----------
print("\nOptimal Value Function:")
for row in V:
    print(["{:.2f}".format(v) for v in row])

print("\nOptimal Dispatch Policy:")
for row in policy:
    print(row.tolist())
