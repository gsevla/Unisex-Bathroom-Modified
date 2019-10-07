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
        self.barrier = threading.Barrier(stallAmo)
        #self.policy_c = policy_c
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
            print('>> {} free stalls'.format(self.stallAmo._value))
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
                print('>> {} free stalls'.format(self.stallAmo._value))
                self.condition.notify_all()
                return True
        except:
            print('semaphore release error')
            return False
        return False

    #### Getters & Setters ####

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

    def getFemaleQueue(self):
        return self.femaleQueue

    def setFemaleQueue(self, q):
        self.femaleQueue = q

    def getUndefinedQueue(self):
        return self.undefinedQueue

    def setUndefinedQueue(self, q):
        self.undefinedQueue = q

    