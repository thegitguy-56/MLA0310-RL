import random

# ---------- USER INPUT ----------
num_agents = int(input("Enter number of service representatives: "))
episodes = int(input("Enter number of Monte Carlo episodes: "))
max_calls = int(input("Enter maximum calls per episode: "))

# ---------- ENVIRONMENT ----------
def simulate_call(free_agents, policy):
    """
    Simulate one call assignment
    Returns reward and updated free_agents
    """
    if free_agents > 0:
        if policy == "priority":
            free_agents -= 1
            return 10, free_agents  # successful service
        else:  # random
            if random.random() > 0.3:
                free_agents -= 1
                return 10, free_agents
            return -1, free_agents
    else:
        return -5, free_agents  # dropped call

# ---------- MONTE CARLO SIMULATION ----------
def monte_carlo(policy):
    returns = {s: [] for s in range(num_agents + 1)}

    for _ in range(episodes):
        free_agents = num_agents
        episode = []

        for _ in range(max_calls):
            state = free_agents
            reward, free_agents = simulate_call(free_agents, policy)
            episode.append((state, reward))

            # random chance that agent becomes free
            if random.random() < 0.4 and free_agents < num_agents:
                free_agents += 1

        # Compute returns
        G = 0
        for state, reward in reversed(episode):
            G += reward
            returns[state].append(G)

    # Estimate value function
    V = {}
    for state in returns:
        V[state] = sum(returns[state]) / len(returns[state]) if returns[state] else 0

    return V

# ---------- RUN SIMULATION ----------
V_random = monte_carlo("random")
V_priority = monte_carlo("priority")

# ---------- OUTPUT ----------
print("\nEstimated Value Function (Random Assignment):")
for s in sorted(V_random):
    print(f"Free Agents {s}: V = {V_random[s]:.2f}")

print("\nEstimated Value Function (Priority Assignment):")
for s in sorted(V_priority):
    print(f"Free Agents {s}: V = {V_priority[s]:.2f}")
