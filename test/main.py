import threading
import datetime
import queue
import random
import time


personType = {
    0: 'M',
    1: 'F',
    2: 'U'
}
personsNumber = 9
generatedPersons = [0, 0, 0]
boxesNumber = 1

servedPeople = 0
busyRate = 0
avgWaitingTime = [0, 0, 0]


# #queues = (queue.Queue(personsNumber/3), queue.Queue(personsNumber/3), queue.Queue(personsNumber/3))
# testQueue = queue.Queue()

class Bathroom(threading.Thread):
    def __init__(self, num, condition):
        self.gender = ''
        self.bathroomStall = threading.BoundedSemaphore(boxesNumber)
        self.maleQueue = queue.Queue(personsNumber/3)
        self.femaleQueue = queue.Queue(personsNumber/3)
        self.undefinedQueue = queue.Queue(personsNumber/3)
        self.condition = condition
        self.turn = []
        self.burst = threading.Event
        threading.Thread.__init__(self, name="Bathroom")

    def run(self):
        print('Bathroom Activated. It has {} stalls.\n'.format(self.getStalls()))

    def queueInsert(self, person):
        if(person.getGender() != self.getGender()):
            self.turn.append(person.getGender())
            print(self.turn)

        try:
            if(person.getGender() == 'M'):
                self.maleQueue.put(person)
            if(person.getGender() == 'F'):
                self.femaleQueue.put(person)
            if(person.getGender() == 'U'):
                self.undefinedQueue.put(person)
        except:
            print('\t## Queue Insert Fail')

    def waitForPolicy(self, person):
        if(person.getGender() == 'M'):
            if(self.turn[0] == 'M'):
                if(person == self.maleQueue[0]):
                    print('igual')
                    self.maleQueue.get()
                    return True
        if(person.getGender() == 'F'):
            if(self.turn[0] == 'F'):
                if(person == self.femaleQueue[0]):
                    print('igual')
                    self.femaleQueue.get()
                    return True
        if(person.getGender() == 'U'):
            if(self.turn[0] == 'U'):
                if(person == self.maleQueue[0]):
                    print('igual')
                    self.femaleQueue.get()
                    return True

    def stallAcquire(self, person):
        if(self.gender == ''):
            #print('teste {}'.format(person.getGender()))
            self.gender = person.getGender()
            
        try:
            self.bathroomStall.acquire()
            print('[{}]Person {} get a stall'.format(person.getGender(), person.getNumber()))
        except:
            print('semaphore acquire error')

    def stallRelease(self, person):
        try:
            if(self.bathroomStall._value == boxesNumber):
                # Class condition 1
                if(len(self.turn) == 0):
                    self.gender = ''
                else:
                    self.gender = self.turn.pop(0)

            with self.condition:
                self.bathroomStall.release()
                print('[{}]Person {} frees a stall at {} second.'.format(person.getGender(), person.getNumber(), time.time()))            
                self.condition.notifyAll()
        except:
            print('semaphore release error')

    def getGender(self):
        return self.gender

    def setGender(self, gender):
        self.gender = gender

    def getStalls(self):
        return self.bathroomStall._value


class Person(threading.Thread):
    def __init__(self, num, arrivalTime, bathroom, condition):
        self.num = num
        self.gender = self.generatePersonGender()
        self.arrivalTime = arrivalTime
        self.bathroom = bathroom
        self.condition = condition
        threading.Thread.__init__(self, name="Person {}".format(num))

    def run(self):
        print('[{}]Person {} arrived at {} second.'.format(self.getGender(), self.getNumber(), self.getArrivalTime()))
        self.enterRestroom(self.bathroom)

    def policy(self, bathroom):
        if(bathroom.getStalls() > 0):
            # Class condition 2
            if(self.gender == bathroom.getGender()):
                return True
            # else:
            #     # Class condition 1

            #     # # MAYBE A DEADLOCK CONDITION
            #     # if(self.gender == 'M'):
            #     #     if(bathroom.maleQueue.empty()):
            #     #         return True
            #     # if(self.gender == 'F'):
            #     #     if(bathroom.femaleQueue.empty()):
            #     #         return True
            #     # if(self.gender == 'U'):
            #     #     if(bathroom.undefinedQueue.empty()):
            #     #         return True
                
            #     bathroom.queueInsert(self)

        return False

    def enterRestroom(self, bathroom):
        if(self.policy(bathroom)):
            self.getStall(bathroom)   
        else:
            print('[{}]Person {} waiting...'.format(self.getGender(), self.getNumber()))
            with self.condition:
                self.condition.wait_for(bathroom.waitForPolicy(self))
            print('[{}]Person {} woke up!'.format(self.getGender(), self.getNumber()))
            self.getStall(bathroom)

    def getStall(self, bathroom):
        global servedPeople
        global busyRate
        try:
            #print(bathroom.getGender())
            bathroom.stallAcquire(self)
            busy = time.time()
            time.sleep(5)
            bathroom.stallRelease(self)
            busyRate += (time.time() - busy)
            servedPeople += 1
        except:
            print('\n## getStall error ##\n')

    def generatePersonGender(self):
        global generatedPersons
        
        while(True):
            personGender = personType[random.randrange(0, 3)]
            if(personGender == 'M' and generatedPersons[0] < personsNumber/3):
                generatedPersons[0] += 1
                return personGender
            if(personGender == 'F' and generatedPersons[1] < personsNumber/3):
                generatedPersons[1] += 1
                return personGender
            if(personGender == 'U' and generatedPersons[2] < personsNumber/3):
                generatedPersons[2] += 1
                return personGender

    def getNumber(self):
        return self.num
    
    def getGender(self):
        return self.gender
    
    def getArrivalTime(self):
        return self.arrivalTime


def main():
    condition = threading.Condition()

    bathroom = Bathroom(boxesNumber, condition)
    bathroom.start()

    personsList = []
    for i in range(personsNumber):
        randArrival = random.randrange(1, 8)
        p = Person(i+1, time.time(), bathroom, condition)
        personsList.append(p)
        p.start()
        time.sleep(randArrival)
    
    for i in personsList:
        i.join()


if __name__ == "__main__":
    totalTime = time.time()

    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram Terminated!\n')

    totalTime = time.time() - totalTime
    print('\n#### Execution Record ####')
    print('\t{} people served'.format(servedPeople))
    print('>> Execution Time: {:.2f}'.format(totalTime))
    print('>> Stalls Busy Rate: {:.2f}'.format(busyRate/totalTime))
    print('>> Average Waiting Time: [M] {:.2f} | [F] {:.2f} | [U] {:.2f}'.format(avgWaitingTime[0], avgWaitingTime[1], avgWaitingTime[2]))