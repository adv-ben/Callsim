import numpy as np
from numpy import random
from queue import Queue, PriorityQueue

random.seed(42)

CALL_INTERVAL = 2
AVG_PATIENCE = 1
PATIENCE_VAR = 2
NUM_EMPLOYEES = 2
CALL_TIME = 10
TIME_STEPS = 120

# event count ensures that there is no conflict between events happening at the same time
ecount = 0

class Call():
    def __init__(self, time, patience):
        self.time = time
        self.patience = patience
    
    def valid(self):
        return self.time <= TIME_STEPS
    
    def dropped(self, time):
        return time > self.time + self.patience

class CallGenerator():
    # generates all incoming calls for the simulation period
    nextCall = 0

    def generate(self, time):
        t = 0
        while(t <= time):
            while(random.randint(CALL_INTERVAL) != 0):
                t += 1
            print(t)
            p = max(1, random.normal(AVG_PATIENCE, PATIENCE_VAR))
            c = Call(t, p)
            if c.valid():
                global ecount
                eventQueue.put((t, ecount, "incoming call", c))
                ecount += 1

class CallQueue():
    q = Queue()

    def checkEmpty(self):
        #print(self.q.queue)
        #print(self.q.empty())
        return self.q.empty()

    def appendCall(self, call):
        self.q.put(call)

    def manageCall(self, cc, time):
        call = self.q.get()
        if(call.dropped(time)):
            return print("call dropped")
        for e in cc.employeeList:
            if(e.free):
                e.assignCall(call, time)
                return print("call managed")
        self.appendCall(call)
        return print("call waiting")
            
class CallCenter():
    employeeList = []
    cq = CallQueue()

    def __init__(self):
        for i in range(NUM_EMPLOYEES):
            self.employeeList.append(Employee())
    
    def manageIncomingCall(self, call):
        self.cq.appendCall(call)
        self.cq.manageCall(self, call.time)
    
    def manageEmployeeFreed(self, time, e):
        # deals with queue until queue is empty or employee is no loger free
        print("call completed")
        e.free = True
        while(not self.cq.checkEmpty() and e.free == True):
            self.cq.manageCall(self, time)


class Employee():
    free = True

    def __init__(self):
        self.free = True

    def assignCall(self, call, time):
        self.free = False
        t = time + CALL_TIME

        if(t <= TIME_STEPS):
            global ecount
            eventQueue.put((t, ecount, "employee freed", self))
            ecount += 1

eventQueue = PriorityQueue(0)

def main():
    cc = CallCenter()

    # generate all incoming calls for the simulation period
    cg = CallGenerator()
    cg.generate(120)
    # print(eventQueue.queue)

    while(not eventQueue.empty()):
        # print(eventQueue.queue)
        event = eventQueue.get()
        eventTime, eventCount, eventType, eventInfo = event
        # print(eventQueue.queue)
        print(eventTime, eventType, eventInfo)
        if(eventType == "incoming call"):
            cc.manageIncomingCall(eventInfo)
        if(eventType == "employee freed"):
            cc.manageEmployeeFreed(eventTime, eventInfo)

    print("Simulation Finished")

main()