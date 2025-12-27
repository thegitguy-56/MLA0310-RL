import math,random

rounds=int(input("Rounds: "))
ctr=[0.3,0.5,0.7]
q=[0]*3; n=[0]*3

for i in range(3):
    q[i]=1 if random.random()<ctr[i] else 0
    n[i]=1

for t in range(3,rounds):
    ucb=[q[i]+math.sqrt(2*math.log(t+1)/n[i]) for i in range(3)]
    a=ucb.index(max(ucb))
    reward=1 if random.random()<ctr[a] else 0
    n[a]+=1
    q[a]+= (reward-q[a])/n[a]

print("Best Content:", q.index(max(q)))
