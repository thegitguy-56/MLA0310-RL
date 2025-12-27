import numpy as np

rows=int(input("Rows: "))
cols=int(input("Cols: "))
goal=tuple(map(int,input("Goal (r c): ").split()))
gamma=0.9

V=np.zeros((rows,cols))
actions=[(-1,0),(1,0),(0,-1),(0,1)]

while True:
    delta=0
    for r in range(rows):
        for c in range(cols):
            if (r,c)==goal: continue
            v=V[r][c]
            V[r][c]=max(
                -1+gamma*V[r+dr][c+dc]
                for dr,dc in actions
                if 0<=r+dr<rows and 0<=c+dc<cols
            )
            delta=max(delta,abs(v-V[r][c]))
    if delta<0.01: break

print("Optimal Value Function:")
print(V)
