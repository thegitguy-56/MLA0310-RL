import random

states=range(6)
cost=[0,1,2,3,4,5]
gamma=0.9
V={s:0 for s in states}

for _ in range(50):
    for s in states:
        V[s]=min(cost[a]+gamma*V[max(0,s-a)] for a in range(s+1))

print("Optimal Value Function:")
print(V)
