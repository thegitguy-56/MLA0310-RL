import random

# ---------- USER INPUT ----------
rows = int(input("Enter number of rows in road grid: "))
cols = int(input("Enter number of columns in road grid: "))

start = tuple(map(int, input("Enter start position (row col): ").split()))
goal = tuple(map(int, input("Enter destination (row col): ").split()))

steps_limit = int(input("Enter maximum steps allowed: "))

# ---------- TRAFFIC LIGHTS ----------
# Intersections with traffic lights
traffic_lights = {
    (1, 1): "GREEN",
    (2, 2): "RED"
}

# ---------- ACTIONS ----------
actions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
    "WAIT": (0, 0)
}

def valid(r, c):
    return 0 <= r < rows and 0 <= c < cols

# ---------- POLICIES ----------
def random_policy():
    return random.choice(list(actions.keys()))

def rule_based_policy(pos):
    # If at red light, wait
    if pos in traffic_lights and traffic_lights[pos] == "RED":
        return "WAIT"

    r, c = pos
    gr, gc = goal

    if r < gr:
        return "DOWN"
    if r > gr:
        return "UP"
    if c < gc:
        return "RIGHT"
    if c > gc:
        return "LEFT"
    return "WAIT"

# ---------- SIMULATION ----------
def simulate(policy_type):
    pos = start
    steps = 0
    violations = 0

    while steps < steps_limit:
        if pos == goal:
            return True, steps, violations

        action = random_policy() if policy_type == "random" else rule_based_policy(pos)
        dr, dc = actions[action]
        nr, nc = pos[0] + dr, pos[1] + dc

        # Traffic violation check
        if pos in traffic_lights and traffic_lights[pos] == "RED" and action != "WAIT":
            violations += 1

        if valid(nr, nc):
            pos = (nr, nc)

        steps += 1

    return False, steps, violations

# ---------- RUN & EVALUATE ----------
random_result = simulate("random")
rule_result = simulate("rule")

# ---------- OUTPUT ----------
print("\n--- Simulation Results ---")

print("\nRandom Policy:")
print(f"Reached Destination: {random_result[0]}")
print(f"Steps Taken: {random_result[1]}")
print(f"Traffic Violations: {random_result[2]}")

print("\nRule-Based Policy:")
print(f"Reached Destination: {rule_result[0]}")
print(f"Steps Taken: {rule_result[1]}")
print(f"Traffic Violations: {rule_result[2]}")
