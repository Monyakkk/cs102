import random
import math




def heavy_computation(data_chunk=[]):
    if data_chunk == []:
        A = []
        B = []
        for i in range (100):
            A.append(random.randint(1,1000))
            B.append(random.randint(1,1000))
        for i in range (100):
            for j in range (100):
                k = A[i]**5*B[j]**5
                print(k)

if __name__ == '__main__':
    heavy_computation()
    
