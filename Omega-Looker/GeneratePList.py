import numpy as np

data = []

for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(2):
                for m in range(2):
                    for n in range(2):
                        for o in range(2):
                            for p in range(2):
                                for q in range(2):
                                   data.append([i,j,k,l,m,n,o,p,q])

data = np.array(data)

print(data)

PList = 'TTTPermutationList.csv'

np.savetxt(PList, data, delimiter=',', fmt='%d')