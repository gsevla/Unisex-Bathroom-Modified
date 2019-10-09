import threading
import time
import queue


class Bathroom(threading.Thread):
    def __init__(self, stallAmo, condition, turn, semaphore):
        self.gender = ''
        self.maxStalls = stallAmo
        self.stallAmo = semaphore
        self.condition = condition
        self.turn = turn
        self.maleQueue = []
        self.femaleQueue = []
        self.undefinedQueue = []
        threading.Thread.__init__(self, name="Bathroom")
        print('Bathroom Activated. It has {} stalls.\n'.format(self.stallAmo._value))

    # def run(self, name='Bathroom', daemon=True):
    #     print('Bathroom Activated. It has {} stalls.\n'.format(self.stallAmo._value))

    def stallAcquire(self, person):
        try:
            self.stallAmo.acquire()
            print('[{}] {} get a stall at {} second.'.format(person.getGender(), person.getMyName(), time.time()))
            print('\n>> Bathrom is {} and it has {} free stalls.\n'.format(self.gender, self.stallAmo._value))
            return True
        except:
            print('semaphore acquire error')
            return False
        return False

    def stallRelease(self, person):
        try:
            with self.condition:
                self.stallAmo.release()
                print('[{}] {} frees a stall at {} second.'.format(person.getGender(), person.getMyName(), time.time()))
                print('\n>> Bathrom is {} and it has {} free stalls.\n'.format(self.gender, self.stallAmo._value))
                self.condition.notify_all()
                return True
        except:
            print('semaphore release error')
            return False
        return False

    #### Getters, Setters & Others ####

    def getFreeStalls(self):
        return self.stallAmo._value

    def getGender(self):
        return self.gender

    def setGender(self, g):
        self.gender = g

    def getMaleQueue(self):
        return self.maleQueue

    def setMaleQueue(self, q):
        self.maleQueue = q

    def insertMaleInQueue(self, p):
        self.maleQueue.append(p)

    def removeMaleFromQueue(self):
        return self.maleQueue.pop(0)

    def getFirstMale(self):
        return self.maleQueue[0]

    def getFemaleQueue(self):
        return self.femaleQueue

    def setFemaleQueue(self, q):
        self.femaleQueue = q

    def insertFemaleInQueue(self, p):
        self.femaleQueue.append(p)

    def removeFemaleFromQueue(self):
        return self.femaleQueue.pop(0)

    def getFirstFemale(self):
        return self.femaleQueue[0]

    def getUndefinedQueue(self):
        return self.undefinedQueue

    def setUndefinedQueue(self, q):
        self.undefinedQueue = q

    def insertUndefinedInQueue(self, p):
        self.undefinedQueue.append(p)

    def removeUndefinedFromQueue(self):
        return self.undefinedQueue.pop(0)

    def getFirstUndefined(self):
        return self.undefinedQueue[0]

    