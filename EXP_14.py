import random

episodes=int(input("Episodes: "))
settings=[0.2,0.5,0.8]
q=[0]*3; n=[0]*3

for _ in range(episodes):
    a=random.randint(0,2)
    reward=10 if random.random()<settings[a] else -5
    n[a]+=1
    q[a]+= (reward-q[a])/n[a]

print("Best Machine Setting:", settings[q.index(max(q))])
