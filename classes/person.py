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
        self.mutex = threading.Semaphore()
        self.semaphore = semaphore
        self.servedPeople = servedPeople
        threading.Thread.__init__(self, name="Person {}".format(num))
        print('[{}] Person {} arrived at {} second.'.format(gender, num, arrivalTime))

    def run(self):
        if(self.policy()):
            self.enterRestroom()
        else:
            with self.condition:
                print('{} run waiting...'.format(self.getName()))
                while not self.personRules():
                    self.condition.wait()
                self.enterRestroom()

    @classmethod
    def generateGender(cls):
        return personGender[random.randrange(0, 3)]

    def peopleInQueue(self):
        if(len(self.bathroom.getMaleQueue()) > 0 or len(self.bathroom.getFemaleQueue()) > 0 or len(self.bathroom.getUndefinedQueue()) > 0):
            return True

        return False
            
    def personRules(self):
        # Some stalls are free
        if(self.semaphore._value > 0):
            # People in queue
            if(self.peopleInQueue()):
                if(self.gender == personGender[0]):
                    if(len(self.bathroom.getMaleQueue()) > 0):
                        if(self == self.bathroom.getFirstMale()):
                            self.bathroom.removeMaleFromQueue()
                            return True
                if(self.gender == personGender[1]):
                    if(len(self.bathroom.getFemaleQueue()) > 0):
                        if(self == self.bathroom.getFirstFemale()):
                            self.bathroom.removeFemaleFromQueue()
                            return True
                if(self.gender == personGender[2]):
                    if(len(self.bathroom.getUndefinedQueue()) > 0):
                        if(self == self.bathroom.getFirstUndefined()):
                            self.bathroom.removeUndefinedFromQueue()
                            return True
                
            # There are no people in queue
            else:
                if(self.semaphore._value == self.maxStalls):
                    self.bathroom.setGender(self.gender)
                    return True
                if(self.gender == self.bathroom.getGender()):
                    return True

        return False

    def goToQueue(self):
        if(self.gender == personGender[0]):
            self.bathroom.insertMaleInQueue(self)
        elif(self.gender == personGender[1]):
            self.bathroom.insertFemaleInQueue(self)
        elif(self.gender == personGender[2]):
            self.bathroom.insertUndefinedInQueue(self)

        return False  

    def policy(self):
        if(not self.peopleInQueue() and self.semaphore._value == self.maxStalls):
            self.bathroom.setGender('')
        # First person
        if(self.bathroom.getGender() == ''):
            self.bathroom.setGender(self.gender)
            return True
        # Crowded Bathroom
        if(self.semaphore._value == 0):
            return self.goToQueue()
        # Person gender aren't equal to bathroom's people
        if(self.bathroom.getGender() != self.gender):
            return self.goToQueue()
        # Person gender are equal to bathroom's people
        else:
            # but some people are waiting in queue
            if(self.peopleInQueue()):
                return self.goToQueue()
        
        return True


    def priority(self):
        if(self.peopleInQueue()):
                if(len(self.bathroom.getMaleQueue()) > 0):
                    m = self.bathroom.getFirstMale()
                    if(len(self.bathroom.getFemaleQueue()) > 0):
                        f = self.bathroom.getFirstFemale()
                        if(len(self.bathroom.getUndefinedQueue()) > 0):
                            u = self.bathroom.getFirstUndefined()
                            if(m.arrivalTime < f.arrivalTime and m.arrivalTime < u.arrivalTime):
                                self.bathroom.setGender(m.gender)
                            if(f.arrivalTime < m.arrivalTime and f.arrivalTime < u.arrivalTime):
                                self.bathroom.setGender(f.gender)
                            if(u.arrivalTime < m.arrivalTime and u.arrivalTime < f.arrivalTime):
                                self.bathroom.setGender(u.gender)
                        else:
                            if(m.arrivalTime < f.arrivalTime):
                                self.bathroom.setGender(m.arrivalTime)
                            else:
                                self.bathroom.setGender(f.arrivalTime)
                    else:
                        self.bathroom.setGender(m.arrivalTime)

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
            # Call for the next person
            self.priority()

    def enterRestroom(self):
        if(self.personRules()):
            self.getStall()
        else:
            with self.condition:
                print('{} enterRestroom waiting...'.format(self.getName()))
                while not self.personRules():
                    self.condition.wait()
                self.enterRestroom()

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