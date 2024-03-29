import threading
import queue
import random
import time
from classes import bathroom, person
import math


personsComing = 60
eachGender = math.ceil(personsComing/3)
maleAmo = 0
femaleAmo = 0
undefinedAmo = 0

stallsAmo = 3

servedPeople = [0, 0, 0]
busyRate = [0]
avgWaitingTime = [0, 0, 0]

def personGender():
    global maleAmo, femaleAmo, undefinedAmo

    while(True):
        gender = person.Person.generateGender()
        if(gender == person.personGender[0]):
            if(maleAmo < eachGender):
                maleAmo += 1
                return gender
        if(gender == person.personGender[1]):
            if(femaleAmo < eachGender):
                femaleAmo += 1
                return gender
        if(gender == person.personGender[2]):
            if(undefinedAmo < eachGender):
                undefinedAmo += 1
                return gender

def main():
    global servedPeople
    global busyRate

    mtx = threading.Semaphore()

    c = threading.Condition()
    sem = threading.BoundedSemaphore(stallsAmo)

    b = bathroom.Bathroom(stallsAmo, c, sem)
    b.start()

    personsList = []
    for i in range(personsComing):
        gender = personGender()
        p = person.Person(gender, i+1, time.time(), b, c, stallsAmo, sem, servedPeople, avgWaitingTime, busyRate, mtx)
        personsList.append(p)
        p.start()

        time.sleep(random.randrange(1, 8))
    
    for j in personsList:
        j.join()

    

if(__name__ == '__main__'):
    
    totalTime = time.time()
    
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram Terminated!\n')

    totalTime = time.time() - totalTime
    print('\n#### Execution Record ####')
    print('\t{} people served'.format(servedPeople))
    print('>> Execution Time: {:.2f}'.format(totalTime))
    print('>> Stalls Busy Rate: {:.2f}'.format(busyRate[0]/totalTime))
    print('>> Average Waiting Time: [M] {:.2f} | [F] {:.2f} | [U] {:.2f}'.format(avgWaitingTime[0]/totalTime, avgWaitingTime[1]/totalTime, avgWaitingTime[2]/totalTime))
