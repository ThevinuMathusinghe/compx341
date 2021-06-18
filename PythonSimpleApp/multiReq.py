import os
for i in range(1365619, 1365619 + 10001):
    os.system('curl http://localhost:50001/isPrime/' + str(i))

