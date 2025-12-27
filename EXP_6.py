import math

# ---------- USER INPUT ----------
num_ads = int(input("Enter number of advertisements: "))

true_ctr = []
print("\nEnter true click-through rate (0 to 1) for each ad:")
for i in range(num_ads):
    p = float(input(f"CTR for Ad {i+1}: "))
    true_ctr.append(p)

rounds = int(input("\nEnter number of user impressions (rounds): "))
epsilon = float(input("Enter epsilon value for Epsilon-Greedy (e.g., 0.1): "))

# ---------- ENVIRONMENT ----------
def show_ad(ad):
    """Simulate user click"""
    return 1 if random.random() < true_ctr[ad] else 0

# ---------- EPSILON GREEDY ----------
def epsilon_greedy():
    counts = [0] * num_ads
    values = [0.0] * num_ads
    clicks = 0

    for _ in range(rounds):
        if random.random() < epsilon:
            ad = random.randint(0, num_ads - 1)
        else:
            ad = values.index(max(values))

        reward = show_ad(ad)
        counts[ad] += 1
        values[ad] += (reward - values[ad]) / counts[ad]
        clicks += reward

    return clicks / rounds

# ---------- UCB ----------
def ucb():
    counts = [0] * num_ads
    values = [0.0] * num_ads
    clicks = 0

    for i in range(num_ads):
        reward = show_ad(i)
        counts[i] = 1
        values[i] = reward
        clicks += reward

    for t in range(num_ads, rounds):
        ucb_values = [
            values[i] + math.sqrt(2 * math.log(t + 1) / counts[i])
            for i in range(num_ads)
        ]
        ad = ucb_values.index(max(ucb_values))

        reward = show_ad(ad)
        counts[ad] += 1
        values[ad] += (reward - values[ad]) / counts[ad]
        clicks += reward

    return clicks / rounds

# ---------- THOMPSON SAMPLING ----------
def thompson_sampling():
    success = [1] * num_ads
    failure = [1] * num_ads
    clicks = 0

    for _ in range(rounds):
        samples = [
            random.betavariate(success[i], failure[i])
            for i in range(num_ads)
        ]
        ad = samples.index(max(samples))

        reward = show_ad(ad)
        clicks += reward

        if reward == 1:
            success[ad] += 1
        else:
            failure[ad] += 1

    return clicks / rounds

# ---------- RUN SIMULATION ----------
eg_ctr = epsilon_greedy()
ucb_ctr = ucb()
ts_ctr = thompson_sampling()

# ---------- OUTPUT ----------
print("\n--- Click-Through Rate Comparison ---")
print(f"Epsilon-Greedy CTR:     {eg_ctr:.4f}")
print(f"UCB CTR:                {ucb_ctr:.4f}")
print(f"Thompson Sampling CTR:  {ts_ctr:.4f}")

best = max(
    ("Epsilon-Greedy", eg_ctr),
    ("UCB", ucb_ctr),
    ("Thompson Sampling", ts_ctr),
    key=lambda x: x[1]
)

print(f"\nBest Performing Algorithm: {best[0]}")
