import numpy as np
import random

# ---------- USER INPUT ----------
episodes = int(input("Enter number of training episodes: "))
learning_rate = float(input("Enter learning rate (e.g., 0.01): "))

# ---------- ACTIONS ----------
actions = ["LOW_RISK", "HIGH_RISK"]
num_actions = len(actions)

# ---------- POLICY PARAMETERS ----------
theta = np.zeros(num_actions)  # policy parameters

# ---------- SOFTMAX POLICY ----------
def softmax(theta):
    exp = np.exp(theta - np.max(theta))
    return exp / np.sum(exp)

# ---------- ENVIRONMENT ----------
def environment(action):
    """
    Simulated investment returns
    """
    if action == 0:  # LOW_RISK
        return random.uniform(1, 3)
    else:  # HIGH_RISK
        return random.uniform(-2, 6)

# ---------- TRAINING (REINFORCE) ----------
episode_rewards = []

for ep in range(episodes):
    probs = softmax(theta)

    # Sample action
    action = np.random.choice(num_actions, p=probs)

    # Get reward
    reward = environment(action)
    episode_rewards.append(reward)

    # Gradient of log policy
    grad = np.zeros(num_actions)
    grad[action] = 1
    grad -= probs

    # Policy update
    theta += learning_rate * reward * grad

# ---------- OUTPUT ----------
final_probs = softmax(theta)

print("\n--- Training Completed ---")
print("Final Policy Probabilities:")
for i, a in enumerate(actions):
    print(f"{a}: {final_probs[i]:.4f}")

print(f"\nAverage Return: {np.mean(episode_rewards):.2f}")
