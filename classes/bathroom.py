import threading
import time
import queue


class Bathroom(threading.Thread):
    def __init__(self, stallAmo, condition, semaphore):
        self.gender = ''
        self.maxStalls = stallAmo
        self.semaphore = semaphore
        self.condition = condition
        self.maleQueue = []
        self.femaleQueue = []
        self.undefinedQueue = []
        self.mutex = threading.Semaphore()
        threading.Thread.__init__(self, name="Bathroom")
        print('>> Bathroom is open and it has {} stalls.\n'.format(self.semaphore._value))


    def stallAcquire(self, person):
        try:
            self.semaphore.acquire()                
            print('[{}] {} get a stall at {} second.'.format(person.getGender(), person.getMyName(), time.strftime("%H:%M:%Sh", time.gmtime()) ))
            print('>> Bathrom is {} and it has {} free stalls.'.format(self.gender, self.semaphore._value))
            return True
        except:
            print('semaphore acquire error')
            return False
        return False

    def stallRelease(self, person):
        try:
            with self.condition:
                self.semaphore.release()
                print('[{}] {} frees a stall at {} second.'.format(person.getGender(), person.getMyName(), time.strftime("%H:%M:%Sh", time.gmtime()) ))
                print('>> Bathrom is {} and it has {} free stalls.'.format(self.gender, self.semaphore._value))
                self.condition.notify_all()
                return True
        except:
            print('semaphore release error')
            return False
        return False

    #### Getters, Setters & Others ####

    def getFreeStalls(self):
        return self.semaphore._value

    def getGender(self):
        return self.gender

    def setGender(self, g):
        with self.mutex:
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
