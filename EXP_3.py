import random
import math

# ---------- USER INPUT ----------
num_prices = int(input("Enter number of price options (arms): "))
prices = []

print("\nEnter price values:")
for i in range(num_prices):
    p = float(input(f"Price {i+1}: "))
    prices.append(p)

print("\nEnter true purchase probabilities (0 to 1):")
true_probs = []
for i in range(num_prices):
    prob = float(input(f"Purchase probability for price {prices[i]}: "))
    true_probs.append(prob)

rounds = int(input("\nEnter number of pricing rounds: "))
epsilon = float(input("Enter epsilon value for Epsilon-Greedy (e.g., 0.1): "))

# ---------- ENVIRONMENT ----------
def pull_arm(arm):
    """Returns revenue based on purchase probability"""
    if random.random() < true_probs[arm]:
        return prices[arm]
    return 0

# ---------- EPSILON GREEDY ----------
def epsilon_greedy():
    counts = [0] * num_prices
    values = [0.0] * num_prices
    total_reward = 0

    for t in range(rounds):
        if random.random() < epsilon:
            arm = random.randint(0, num_prices - 1)
        else:
            arm = values.index(max(values))

        reward = pull_arm(arm)
        counts[arm] += 1
        values[arm] += (reward - values[arm]) / counts[arm]
        total_reward += reward

    return total_reward

# ---------- UCB ----------
def ucb():
    counts = [0] * num_prices
    values = [0.0] * num_prices
    total_reward = 0

    for i in range(num_prices):
        reward = pull_arm(i)
        counts[i] = 1
        values[i] = reward
        total_reward += reward

    for t in range(num_prices, rounds):
        ucb_values = [
            values[i] + math.sqrt(2 * math.log(t + 1) / counts[i])
            for i in range(num_prices)
        ]
        arm = ucb_values.index(max(ucb_values))

        reward = pull_arm(arm)
        counts[arm] += 1
        values[arm] += (reward - values[arm]) / counts[arm]
        total_reward += reward

    return total_reward

# ---------- THOMPSON SAMPLING ----------
def thompson_sampling():
    success = [1] * num_prices
    failure = [1] * num_prices
    total_reward = 0

    for _ in range(rounds):
        sampled_theta = [
            random.betavariate(success[i], failure[i])
            for i in range(num_prices)
        ]
        arm = sampled_theta.index(max(sampled_theta))

        reward = pull_arm(arm)
        total_reward += reward

        if reward > 0:
            success[arm] += 1
        else:
            failure[arm] += 1

    return total_reward

# ---------- RUN SIMULATION ----------
eg_reward = epsilon_greedy()
ucb_reward = ucb()
ts_reward = thompson_sampling()

# ---------- OUTPUT ----------
print("\n--- Total Revenue Comparison ---")
print(f"Epsilon-Greedy Revenue: {eg_reward:.2f}")
print(f"UCB Revenue:            {ucb_reward:.2f}")
print(f"Thompson Sampling:     {ts_reward:.2f}")

best = max(
    ("Epsilon-Greedy", eg_reward),
    ("UCB", ucb_reward),
    ("Thompson Sampling", ts_reward),
    key=lambda x: x[1]
)

print(f"\nBest Strategy: {best[0]}")
