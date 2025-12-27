import random
import math

# ---------- USER INPUT ----------
k = int(input("Enter number of marketing campaigns (arms): "))
rounds = int(input("Enter number of trials: "))
epsilon = float(input("Enter epsilon (e.g., 0.1): "))

print("\nEnter true conversion probability for each campaign:")
true_probs = []
for i in range(k):
    p = float(input(f"Campaign {i}: "))
    true_probs.append(p)

# ---------- ENVIRONMENT ----------
def pull(arm):
    return 1 if random.random() < true_probs[arm] else 0

# ---------- EPSILON GREEDY ----------
def epsilon_greedy():
    Q = [0]*k
    N = [0]*k
    total = 0

    for _ in range(rounds):
        arm = random.randint(0,k-1) if random.random()<epsilon else Q.index(max(Q))
        r = pull(arm)
        N[arm]+=1
        Q[arm]+= (r-Q[arm])/N[arm]
        total+=r
    return total

# ---------- UCB ----------
def ucb():
    Q = [0]*k
    N = [1]*k
    total = 0

    for i in range(k):
        r = pull(i)
        Q[i] = r
        total += r

    for t in range(k, rounds):
        ucb_values = [
            Q[i] + math.sqrt(2*math.log(t+1)/N[i])
            for i in range(k)
        ]
        arm = ucb_values.index(max(ucb_values))
        r = pull(arm)
        N[arm]+=1
        Q[arm]+= (r-Q[arm])/N[arm]
        total+=r

    return total

# ---------- THOMPSON SAMPLING ----------
def thompson_sampling():
    success = [1]*k
    failure = [1]*k
    total = 0

    for _ in range(rounds):
        samples = [
            random.betavariate(success[i], failure[i])
            for i in range(k)
        ]
        arm = samples.index(max(samples))
        r = pull(arm)
        total+=r
        if r==1:
            success[arm]+=1
        else:
            failure[arm]+=1
    return total

# ---------- RUN ----------
eg = epsilon_greedy()
ucb_res = ucb()
ts = thompson_sampling()

print("\n--- Results ---")
print("Epsilon-Greedy Reward:", eg)
print("UCB Reward:", ucb_res)
print("Thompson Sampling Reward:", ts)

best = max(("Epsilon-Greedy",eg),("UCB",ucb_res),("Thompson Sampling",ts), key=lambda x:x[1])
print("\nBest Strategy:", best[0])
