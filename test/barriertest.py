import threading
import time
import random

b = threading.Barrier(2)

persons = ['p1', 'p2', 'p3', 'p4']

def person():
    name = persons.pop()
    print(b.parties)
    print('{} na barreira'.format(name))
    time.sleep(random.randrange(5, 8))
    b.wait()

#0personsThreads = []
print('vai começar a brincadeira')
for i in range(4):
    time.sleep(1)
    threading.Thread(target=person).start()

# while(True):
#     time.sleep(1)
#     print(b.n_waiting)
