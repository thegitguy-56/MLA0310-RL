import numpy as np
import matplotlib.pyplot as plt

# ---------- USER INPUT ----------
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
gamma = float(input("Enter discount factor (e.g., 0.9): "))
theta = 0.01

# Grid
grid = np.zeros((rows, cols))

print("\nEnter obstacle locations:")
obs = int(input("Number of obstacles: "))
for _ in range(obs):
    r, c = map(int, input("Obstacle (row col): ").split())
    grid[r][c] = -999

print("\nEnter delivery points:")
goals = int(input("Number of delivery points: "))
delivery_points = []
for _ in range(goals):
    r, c = map(int, input("Delivery point (row col): ").split())
    delivery_points.append((r, c))

# ---------- ACTIONS ----------
actions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

# ---------- INITIALIZE ----------
V = np.zeros((rows, cols))

def valid(r, c):
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] != -999

# ---------- POLICIES ----------
def random_policy():
    return list(actions.keys())

def greedy_policy(state):
    r, c = state
    best = []
    best_val = float("-inf")
    for a, (dr, dc) in actions.items():
        nr, nc = r + dr, c + dc
        if valid(nr, nc):
            value = -1 + gamma * V[nr][nc]
            if value > best_val:
                best_val = value
                best = [a]
    return best

# ---------- POLICY EVALUATION ----------
def policy_evaluation(policy_type):
    global V
    V = np.zeros((rows, cols))

    while True:
        delta = 0
        for r in range(rows):
            for c in range(cols):
                if (r, c) in delivery_points or grid[r][c] == -999:
                    continue

                v = V[r][c]
                new_v = 0
                actions_list = random_policy() if policy_type == "random" else greedy_policy((r, c))

                prob = 1 / len(actions_list)
                for a in actions_list:
                    dr, dc = actions[a]
                    nr, nc = r + dr, c + dc
                    if valid(nr, nc):
                        reward = 10 if (nr, nc) in delivery_points else -1
                        new_v += prob * (reward + gamma * V[nr][nc])

                V[r][c] = new_v
                delta = max(delta, abs(v - new_v))

        if delta < theta:
            break

    return V.copy()

# ---------- EVALUATE POLICIES ----------
V_random = policy_evaluation("random")
V_greedy = policy_evaluation("greedy")

# ---------- VISUALIZATION ----------
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

axs[0].imshow(V_random)
axs[0].set_title("Value Function – Random Policy")
for i in range(rows):
    for j in range(cols):
        axs[0].text(j, i, f"{V_random[i,j]:.1f}", ha="center", va="center")

axs[1].imshow(V_greedy)
axs[1].set_title("Value Function – Greedy Policy")
for i in range(rows):
    for j in range(cols):
        axs[1].text(j, i, f"{V_greedy[i,j]:.1f}", ha="center", va="center")

plt.colorbar(axs[0].images[0], ax=axs)
plt.show()
