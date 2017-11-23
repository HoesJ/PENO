N = 556

A_F = [[0 for i in range(N)] for j in range(N)]

file = open('viewmatrix.txt', 'r')
for line in file:
    if (line[0] == "#"):
        continue
    i, j, F_i_j = line.strip().split(' ')
    i, j, F_i_j = int(i), int(j), float(F_i_j)
    A_F[i][j] = F_i_j

sums = []
for i in range(N):
    sums.append(sum(A_F[i]))
print("sommen:",sums)
print("soms van sommen:",sum(sums))