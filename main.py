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
queue = queue.Queue(personsNumber)
boxesNumber = 3
totalTime = 0
avgWaitingTime = [0, 0, 0]
ocpRate = []
maxThreadNum = 0


class Bathroom(threading.Thread):
    def __init__(self, num):
        self.gender = ''
        self.bathroomSize = threading.Semaphore(num)
        self.boxes = self.generateBoxes(num)
        threading.Thread.__init__(self, name="Bathroom")
    
    def run(self):
        print(self.bathroomSize)
        print(self.boxes)

    def generateBoxes(self, num):
        boxes = []
        for i in range(num):
            boxes.append(threading.Lock)
        return boxes

    def getGender(self):
        return self.gender

    def setGender(self, gender):
        self.gender = gender

    def bathroomAcquire(self, personGender):
        if(self.gender == ''):
            self.gender = personGender
        self.bathroomSize.acquire()
        print('pegou')

    def bathroomRelease(self):
        self.bathroomSize.release()
        print(self.bathroomSize._value)
        if(self.bathroomSize._value == boxesNumber):
            self.gender = ''
            threading.Condition().notify_all()
        print('soltou')

    


class Person(threading.Thread):
    def __init__(self, num, arrivalTime):
        self.num = num
        self.gender = self.generatePersonGender()
        self.arrivalTime = arrivalTime
        threading.Thread.__init__(self, name="Person {}".format(num))

    def run(self):
        self.showPersonInfo()

    def enterRestroom(self, restroom):
        if(restroom.getGender() == '' or self.gender == restroom.getGender()):
            restroom.bathroomAcquire(self.gender)
            time.sleep(5)
            restroom.bathroomRelease()
        else:
            print(self.name)
            threading.Condition().wait()


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

    def showPersonInfo(self):
        print('[{}]Person {} arrived at {} second.'.format(self.gender, self.num, self.arrivalTime))

    def getPeopleNumber(self):
        return self.num
    
    def getGender(self):
        return self.gender
    
    def getArrivalTime(self):
        return self.arrivalTime
        

def generatePerson(bathroom):
    
    for i in range(personsNumber):
        randArrival = random.randrange(1, 8)
        time.sleep(randArrival)
        p = Person(i+1, time.time())
        p.start()
        queue.put(p)
        p.enterRestroom(bathroom)
    

def main():
    global globalTime
    globalTime = time.time()
    for i in range(boxesNumber): 
        ocpRate.append(0)
    
    bth = Bathroom(boxesNumber)
    bth.start()

    arrivals = threading.Thread(target=generatePerson, name='Arrivals', args=(bth,))
    arrivals.start()


if __name__ == "__main__":
    main()
