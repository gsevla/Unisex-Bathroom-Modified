import threading
import time
import random
from ub3g import servedPeople

personGender = {
    0: 'M',
    1: 'F',
    2: 'U'
}


class Person(threading.Thread):
    def __init__(self, gender, num, arrivalTime, bathroom, condition, maxStalls, policy_c, turn, semaphore):
        self.gender = gender
        self.num = num
        self.arrivalTime = arrivalTime
        self.bathroom = bathroom
        self.condition = condition
        self.maxStalls = maxStalls
        self.policy_c = policy_c
        self.turn = turn
        self.semaphore = semaphore
        threading.Thread.__init__(self, name="Person {}".format(num))
        print('[{}] Person {} arrived at {} second.'.format(gender, num, arrivalTime))

    def run(self):
        self.enterRestroom()

    @classmethod
    def generateGender(cls):
        return personGender[random.randrange(0, 3)]

    def basic_policy(self):
        if(self.bathroom.getGender() == '' or self.semaphore._value == self.maxStalls):
            self.bathroom.setGender(self.gender)
        
        if(self.semaphore._value == 0):
            self.bathroom.setGender('')

        if(self.bathroom.getFreeStalls() > 0):

            if(self.bathroom.getGender() == '' or self.bathroom.getGender() == self.gender):
                return True
        
        return False
            

    def policy(self):
        if(self.bathroom.getFreeStalls() > 0):

            if(self.semaphore._value == self.maxStalls):
                self.policy_c = True
                if(len(self.turn) > 0):
                    if(self.turn[-1] != self.gender):
                        self.turn.append(self.gender)
                        print('>> turn {}'.format(self.turn))
                else:
                    self.turn.append(self.gender)
                    print('>> turn {}'.format(self.turn))
            elif(self.semaphore._value == 0):
                self.policy_c = False
                self.bathroom.setGender('')

            if(self.bathroom.getGender() != self.gender):
                if(len(self.turn) > 0):
                    self.bathroom.setGender(self.turn.pop(0))
                    print('>> turn {}'.format(self.turn))
                else:
                    self.bathroom.setGender(self.gender)
            
            if(self.bathroom.getGender() == self.gender):
                if(self.gender == personGender[0]):
                    q = self.bathroom.getMaleQueue()
                    if(len(q) > 0):
                        if(q[0] == self):
                            q.pop(0)
                            self.bathroom.setMaleQueue(q)
                            return True
                        else:
                            return False
                    else:
                        return True
                if(self.gender == personGender[1]):
                    q = self.bathroom.getFemaleQueue()
                    if(len(q) > 0):
                        if(q[0] == self):
                            q.pop(0)
                            self.bathroom.setFemaleQueue(q)
                            return True
                        else:
                            return False
                    else:
                        return True
                if(self.gender == personGender[2]):
                    q = self.bathroom.getUndefinedQueue()
                    if(len(q) > 0):
                        if(q[0] == self):
                            q.pop(0)
                            self.bathroom.setUndefinedQueue(q)
                            return True
                        else:
                            return False
                    else:
                        return True

        return False
            

    def getStall(self):
        global servedPeople
        acquire = self.bathroom.stallAcquire(self)
        if(acquire):
            time.sleep(5)
        release = self.bathroom.stallRelease(self)
        if(release):
            servedPeople += 1
            print(servedPeople)


    def enterRestroom(self):
        if(self.basic_policy()):
            self.getStall()
        else:
            # with self.condition:
            #     print('[{}] {} waiting...'.format(self.gender, self.getName()))
            #     self.condition.wait_for(self.getPolicy_c)
            #     print('condition {}'.format(self.policy_c))
            #     self.enterRestroom()

            # with self.condition:
            #     while not self.basic_policy():
            #         self.condition.wait()
            #     self.enterRestroom()

            with self.condition:
                print('{} waiting...'.format(self.getName()))
                self.condition.wait_for(self.basic_policy)
                self.enterRestroom()

    #### Getters & Setters ####

    def getArrivalTime(self):
        return self.arrivalTime

    def getMyName(self):
        return self.getName()

    def getNumber(self):
        return self.num

    def getGender(self):
        return self.gender

    def getPolicy_c(self):
        return self.policy_c