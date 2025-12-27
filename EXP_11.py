import random, math

rounds = int(input("Enter number of games: "))
epsilon = float(input("Enter epsilon: "))
tau = float(input("Enter softmax temperature: "))

# true win probs for actions
probs = [0.3, 0.6]

def epsilon_greedy():
    wins = 0
    q = [0, 0]
    n = [0, 0]
    for _ in range(rounds):
        a = random.randint(0,1) if random.random()<epsilon else q.index(max(q))
        win = 1 if random.random()<probs[a] else 0
        n[a]+=1
        q[a]+= (win-q[a])/n[a]
        wins+=win
    return wins/rounds

def softmax():
    wins = 0
    q=[0,0]; n=[0,0]
    for _ in range(rounds):
        exp=[math.exp(q[i]/tau) for i in range(2)]
        p=[e/sum(exp) for e in exp]
        a=random.choices([0,1],p)[0]
        win=1 if random.random()<probs[a] else 0
        n[a]+=1
        q[a]+= (win-q[a])/n[a]
        wins+=win
    return wins/rounds

print("Epsilon-Greedy Win Rate:", epsilon_greedy())
print("Softmax Win Rate:", softmax())
