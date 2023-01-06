from glob import glob
from numpy import random
from time import sleep, time
import threading
import sys
from queue import Queue
import matplotlib.pyplot as plt

#Get transmition time of frames from user input.
Tfr = float(input("Please enter Tfr(seconds)\nEnter 0 for default 10 miliseconds: "))
if Tfr == 0.0:
    Tfr = 0.01

duration = int(input("Please enter duration of simulation(seconds): "))

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

    

    while True:
        #Generate a random exponential variable with lambda=1/2 in miliseconds.
        #lambda=2 in poison means that lambda is 1/2 in exponential.
        waitTime = random.exponential(0.5,None)
        BeginTime = time()

        #Now wait for the random amount of time to pass.
        sleep(waitTime)

        #Start transmiting
        transmissions += 1

        #If channel is busy(lock is locked!).
        if lock.locked():
            #Collision happens but still transmiting the frame
            failedFrames += 1
            
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
            

                if q.empty():
                    pass
                #q being not empty means some other node(s) are transmitting too and this transmission is failed because of collision.
                else:
                    collision = True

                if elapsedTime > seconds:
                    break
            
            # time_success.append(Gaptime*1000)
            q.queue.clear()
            channelBusy = False
            lock.release()
            semaphore.acquire()
            if collision:
                failedFrames += 1
                failedFramesarray.append(failedFrames)
                failedcurrenttime = time()
                Gaptime = failedcurrenttime- BeginTime
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
print("Throughput(kbps): " + str((successfulFrames)/duration))

print("success counter: " + str(success))
print("array: " + str(successfulFramesarray))

plt.figure()
plt.plot(duration, successfulFramesarray)

plt.xlabel("time")
plt.ylabel("successful Frames")
plt.show()
sys.exit()