import numpy as np

V=np.zeros((3,3))
gamma=0.9

for _ in range(50):
    for r in range(3):
        for c in range(3):
            if (r,c)==(2,2): continue
            V[r][c]=-1+gamma*max(
                V[nr][nc]
                for nr,nc in [(r+1,c),(r,c+1)]
                if nr<3 and nc<3
            )

print("Value Function:")
print(V)
