import numpy as np

# ---------- USER INPUT ----------
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

gamma = float(input("Enter discount factor (e.g., 0.9): "))
theta = 0.01

# Initialize rewards grid
rewards = np.zeros((rows, cols))

print("\nEnter obstacle positions:")
obs = int(input("Number of obstacles: "))
for _ in range(obs):
    r, c = map(int, input("Obstacle (row col): ").split())
    rewards[r][c] = -2

print("\nEnter item positions:")
items = int(input("Number of items: "))
for _ in range(items):
    r, c = map(int, input("Item (row col): ").split())
    rewards[r][c] = 2

print("\nEnter goal position:")
gr, gc = map(int, input("Goal (row col): ").split())
rewards[gr][gc] = 5

# Initialize value function
V = np.zeros((rows, cols))

# ---------- POLICY DEFINITION ----------
# Fixed policy: RIGHT → DOWN → LEFT → UP
def policy(state):
    r, c = state
    if c + 1 < cols:
        return (r, c + 1)
    elif r + 1 < rows:
        return (r + 1, c)
    elif c - 1 >= 0:
        return (r, c - 1)
    elif r - 1 >= 0:
        return (r - 1, c)
    return state

# ---------- POLICY EVALUATION ----------
while True:
    delta = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) == (gr, gc):  # terminal state
                continue
            if rewards[r][c] == -2:  # obstacle
                continue

            nr, nc = policy((r, c))
            v = V[r][c]
            V[r][c] = rewards[nr][nc] + gamma * V[nr][nc]
            delta = max(delta, abs(v - V[r][c]))

    if delta < theta:
        break

# ---------- OUTPUT ----------
print("\nFinal Value Function:")
for row in V:
    print(["{:.2f}".format(val) for val in row])
