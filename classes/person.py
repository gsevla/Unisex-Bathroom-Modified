import threading
import time
import random
#from ub3g import servedPeople

personGender = {
    0: 'M',
    1: 'F',
    2: 'U'
}


class Person(threading.Thread):
    def __init__(self, gender, num, arrivalTime, bathroom, condition, maxStalls, rules, turn, semaphore, servedPeople):
        self.gender = gender
        self.num = num
        self.arrivalTime = arrivalTime
        self.bathroom = bathroom
        self.condition = condition
        self.maxStalls = maxStalls
        self.rules = rules
        self.turn = turn
        self.semaphore = semaphore
        self.servedPeople = servedPeople
        threading.Thread.__init__(self, name="Person {}".format(num))
        print('[{}] Person {} arrived at {} second.'.format(gender, num, arrivalTime))

    def run(self):
        if(self.policy()):
            self.enterRestroom()
        else:
            with self.condition:
                print('{} waiting...'.format(self.getName()))
                self.condition.wait_for(self.personRules)
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

    def peopleInQueue(self):
        if(len(self.bathroom.getMaleQueue()) > 0 or len(self.bathroom.getFemaleQueue()) > 0 or len(self.bathroom.getUndefinedQueue()) > 0):
            return True

        return False

    def leaveFromQueue(self):
        if(self.gender == self.bathroom.getGender()):
            if(self.gender == personGender[0]):
                if(len(self.bathroom.getMaleQueue()) > 0):
                    if(self.bathroom.getFirstMale() == self):
                        self.bathroom.removeMaleFromQueue()
                        return True
            elif(self.gender == personGender[1]):
                if(len(self.bathroom.getFemaleQueue()) > 0):
                    if(self.bathroom.getFirstFemale() == self):
                        self.bathroom.removeFemaleFromQueue()
                        return True
            elif(self.gender == personGender[2]):
                if(len(self.bathroom.getUndefinedQueue()) > 0):
                    if(self.bathroom.getFirstUndefined() == self):
                        self.bathroom.removeUndefinedFromQueue()
                        return True

        return False
    
            
    def personRules(self):
        # People in queue
        if(self.peopleInQueue()):
            # and all stalls are free
            if(self.semaphore._value == self.maxStalls):
                if(len(self.turn) > 0):
                    self.bathroom.setGender(self.turn.pop(0))
                else:
                    self.bathroom.setGender(self.gender)
                self.leaveFromQueue()
        # There are no people in queue
        else:
            # and some stalls are free
            if(self.semaphore._value > 0):
                if(self.gender == self.bathroom.getGender()):
                    return True

        return False



    def verifyTurn(self):
        if(len(self.turn) > 0):
            if(self.turn[-1] != self.gender):
                self.goToQueue()
        else:
            self.goToQueue()

    def goToQueue(self):
        self.turn.append(self.gender)

        if(self.gender == personGender[0]):
            self.bathroom.insertMaleInQueue(self)
        elif(self.gender == personGender[1]):
            self.bathroom.insertFemaleInQueue(self)
        elif(self.gender == personGender[2]):
            self.bathroom.insertUndefinedInQueue(self)

        return False  

    def policy(self):
        # Crowded Bathroom
        if(self.semaphore._value == 0):
            self.verifyTurn()
        # Person gender aren't equal to bathroom's people
        if(self.bathroom.getGender() != self.gender and self.bathroom.getGender() != ''):
            self.verifyTurn()
        # Person gender are equal to bathroom's people
        else:
            # but some people are waiting in queue
            if(self.peopleInQueue()):
                self.verifyTurn()
        
        return True


    def getStall(self):
        acquire = self.bathroom.stallAcquire(self)
        if(acquire):
            time.sleep(5)
        release = self.bathroom.stallRelease(self)
        if(release):
            if(self.gender == personGender[0]):
                self.servedPeople[0] += 1
            if(self.gender == personGender[1]):
                self.servedPeople[1] += 1
            if(self.gender == personGender[2]):
                self.servedPeople[2] += 1
            print(self.servedPeople)

    def enterRestroom(self):
        self.getStall()

    #### Getters, Setters & Others ####

    def getArrivalTime(self):
        return self.arrivalTime

    def getMyName(self):
        return self.getName()

    def getNumber(self):
        return self.num

    def getGender(self):
        return self.gender

    def getRules(self):
        return self.rules