import random

episodes=int(input("Episodes: "))
returns=[]

for _ in range(episodes):
    churn=random.random()<0.3
    reward=10 if not churn else -10
    returns.append(reward)

print("Estimated Value:", sum(returns)/len(returns))
