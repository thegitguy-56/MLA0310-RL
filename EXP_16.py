import random

rounds=int(input("Rounds: "))
epsilon=float(input("Epsilon: "))
ctr=[0.2,0.4,0.6]
q=[0]*3; n=[0]*3

for _ in range(rounds):
    a=random.randint(0,2) if random.random()<epsilon else q.index(max(q))
    click=1 if random.random()<ctr[a] else 0
    n[a]+=1
    q[a]+= (click-q[a])/n[a]

print("Best Content Index:", q.index(max(q)))
