import threading
import queue
import random
import time
from classes import bathroom, person
import math



personsComing = 12
eachGender = math.ceil(personsComing/3)
maleAmo = 0
femaleAmo = 0
undefinedAmo = 0

stallsAmo = 3

servedPeople = [0, 0, 0]


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

    c = threading.Condition()
    sem = threading.BoundedSemaphore(stallsAmo)
    turn = []
    rules = False

    b = bathroom.Bathroom(stallsAmo, c, turn, sem)
    b.start()

    personsList = []
    for i in range(personsComing):
        gender = personGender()
        p = person.Person(gender, i+1, time.time(), b, c, stallsAmo, rules, turn, sem, servedPeople)
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
    print('>> Execution Time: {:.2f}'.format(totalTime))
    #print(maleAmo, femaleAmo, undefinedAmo)
    print('\t{} people served'.format(servedPeople))
