from glob import glob
from numpy import random
from time import sleep, time
import threading
import sys
from queue import Queue
import matplotlib.pyplot as plt
import math

#Get transmition time of frames from user input.
Tfr = float(input("Please enter Tfr(seconds)\nEnter 0 for default 10 miliseconds: "))
if Tfr == 0.0:
    Tfr = 0.01

duration = 2

Node_Number = int(input ("please enter Number of Nodes:  "))
Node = []



transmissions = 0
failedFrames = 0
channelBusy = False
successfulFrames = 0
success = 0
lock = threading.Lock()
#Threads will communicate with each other using this queue
q = Queue()
semaphore = threading.Semaphore(11)

failedFramesarray = []
successfulFramesarray = []
time_success = []
time_fail = []
totalTime = []

#Main part of programm. It acts like a ALOHA oriented node.
#Each node(thread) will use this function.
def runALOHAnode():
    global Tfr
    global transmissions
    global failedFrames
    global successfulFrames
    global channelBusy
    global lock
    global q
    global success
    global totalTime

    

    while True:
        #Generate a random exponential variable with lambda=1/2 in miliseconds.
        #lambda=2 in poison means that lambda is 1/2 in exponential.
        waitTime = random.exponential(1,None)
        BeginTime = time()

        #Now wait for the random amount of time to pass.
        sleep(waitTime)

        #Start transmiting
        transmissions += 1

        #If channel is busy(lock is locked!).
        if lock.locked():
            #Collision happens but still transmiting the frame
            failedFrames += 1
            totalTime.append(transmissions)
            
            failedFramesarray.append(failedFrames)
            failedcurrenttime = time()
            Gaptime = failedcurrenttime- BeginTime
            time_fail.append(Gaptime*1000)

            #Put data in queue to tell other sending nodes that this is a collision and their transmitted frame is failed
            q.put(1)
            #Sleeping for Tfr seconds means that node is transmitting and it takes Tfr seconds.
            sleep(Tfr)

        #If channel is not occupied(lock is unlocked).
        else:
            success += 1
            successfulFramesarray.append(success)
            lock.acquire()
            collision = False
            channelBusy = True
            startTime = time()
            seconds = Tfr
            
            #Sleeping for Tfr seconds means that node is transmitting and it takes Tfr seconds.
            while True:
                currentTime = time()

                elapsedTime = currentTime - startTime
            

                
                #q being not empty means some other node(s) are transmitting too and this transmission is failed because of collision.
                if not q.empty():
                    collision = True

                if elapsedTime > seconds:
                    break
            
            
            q.queue.clear()
            channelBusy = False
            lock.release()
            semaphore.acquire()
            if collision:
                failedFrames += 1
                failedFramesarray.append(failedFrames)
                failedcurrenttime = time()
                Gaptime = failedcurrenttime - BeginTime
                time_fail.append(Gaptime*1000)
            semaphore.release()
            

for i in range(Node_Number):
    Node_threads = threading.Thread(target = runALOHAnode)
    Node_threads.daemon = True
    Node_threads.start()        
        

#wait for threads to run for a while.
print("Please wait...\n")
sleep(duration)

successfulFrames = transmissions - failedFrames


# print(time_success)

print(time_fail)

print(failedFramesarray)

print("Transmited frames: " + str(transmissions))
print("Failed frames: " + str(failedFrames))
print("Successful frames: " + str(successfulFrames))
print("Effiency(kbps): " + str(Node_Number * math.exp(-2 * Node_Number)))