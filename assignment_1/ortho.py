import numpy as np
import random

def orthogonal(ns):
   assert(np.sqrt(ns) % 1 == 0),"Please insert an even number of samples"
   n = int(np.sqrt(ns))
   # Making a datastructure of a dict with coordinate tuples of a bigger grid with subcoordinate of sub-grid points
   blocks = {(i,j):[(a,b) for a in range(n) for b in range(n)] for i in range(n) for j in range(n)}
   points = []#np.empty((n,2))
   append = points.append # tips of python to fasten up append call
   for block in blocks:
      point = random.choice(blocks[block])
      lst_row = [(k1, b) for (k1, b), v in blocks.items() if k1 == block[0]]
      lst_col = [(a, k1) for (a, k1), v in blocks.items() if k1 == block[1]]

      for col in lst_col:
          blocks[col] = [a for a in blocks[col] if a[1] != point[1]]

      for row in lst_row:
          blocks[row] = [a for a in blocks[row] if a[0] != point[0]]
      #Adjust the points to fit the grid they fall in  
      point = (point[0] + n * block[0], point[1] + n * block[1])
      append(point)
   return points


print(orthogonal(4000))

