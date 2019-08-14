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
personsNumber = 60
generatedPersons = [0, 0, 0]
queues = [queue.Queue(personsNumber/3), queue.Queue(personsNumber/3), queue.Queue(personsNumber/3)]
boxesNumber = 1
totalTime = 0


class Person(threading.Thread):
    def __init__(self, num, arrivalTime):
        self.num = num
        self.gender = self.generatePersonGender()
        self.arrivalTime = arrivalTime
        self.showPersonInfo()
        threading.Thread.__init__(self)

    def generatePersonGender(self):
        global generatedPersons
        
        while(True):
            personGender = personType[random.randrange(0, 3)]
            if(personGender == 'M' and generatedPersons[0] < 20):
                generatedPersons[0] += 1
                return personGender
            if(personGender == 'F' and generatedPersons[1] < 20):
                generatedPersons[1] += 1
                return personGender
            if(personGender == 'U' and generatedPersons[2] < 20):
                generatedPersons[2] += 1
                return personGender
    
    def bathroomTime(self):
        time.sleep(5)
        print('[{}]Person {} out at {}'.format(self.gender, self.num, totalTime))

    def showPersonInfo(self):
        print('[{}]Person {} arrived at {} second.'.format(self.gender, self.num, self.arrivalTime))

    def getPeopleNumber(self):
        return self.num
    
    def getGender(self):
        return self.gender
    
    def getArrivalTime(self):
        return self.arrivalTime
        

def generatePerson():
    global totalTime
    
    for i in range(personsNumber):
        randArrival = random.randrange(1, 8)
        time.sleep(randArrival)
        totalTime += randArrival
        p = Person(i+1, totalTime)
        print(p)
        addPersonToQueue(p)

    showQueues()


def addPersonToQueue(p):
    if(p.gender == 'M'):
        queues[0].put(p)
    if(p.gender == 'F'):
        queues[1].put(p)
    if(p.gender == 'U'):
        queues[2].put(p)


def showQueues():
    print('## [{}]Male'.format(queues[0].qsize()))
    for i in range(queues[0].qsize()):
        print(queues[0].get().showPersonInfo())

    print('## [{}]Female'.format(queues[1].qsize()))
    for i in range(queues[1].qsize()):
        print(queues[1].get().showPersonInfo())

    print('## [{}]Undefined'.format(queues[2].qsize()))
    for i in range(queues[2].qsize()):
        print(queues[2].get().showPersonInfo())
    

def main():
    arrivals = threading.Thread(target=generatePerson, name='Arrivals')
    arrivals.start()


if __name__ == "__main__":
    main()
    
