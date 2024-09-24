from bsp import board
import gpio
import serial
import threading

CLOCKWISE=True
ANTICLOCKWISE=False
TOTAL_STEPS=512 #giro di 360 gradi
STD_DELAY=2 #velocità di rotazione

CW=[[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]] #clockwise
ACW=CW[::-1] #lista invertita (anticlockwise)

lock = threading.Lock()

def stepper_thread(stp):#funzione del thread
    while stp.fine==False:
        sleep(2239)
        while stp.parti==True:
            lock.acquire()
            stp.both_angle_rotation(stp.angolo,stp.delay)
            lock.release()


class motor():

    def __init__(self,in1,in2,in3,in4): #inizializzo la classe
        self.In=[in1,in2,in3,in4]
        for i in range(len(self.In)):
            gpio.mode(self.In[i], OUTPUT)
        self.fine=False
        self.parti=False
        self.angolo=0
        self.delay=0


    def rotation(self, dir, steps=TOTAL_STEPS, delay=STD_DELAY):#eseguo una rotazione in base ai passi
        if(dir==CLOCKWISE):
            for i in range(int(steps)):
                for j in range(len(CW)):
                    for k in range(len(CW[j])):
                        if (CW[j][k]==1):
                            gpio.high(self.In[k])
                        else:
                            gpio.low(self.In[k])
                    sleep(delay)

        elif(dir==ANTICLOCKWISE):
            for i in range(int(steps)):
                for j in range(len(ACW)):
                    for k in range(len(ACW[j])):
                        if (ACW[j][k]==1):
                            gpio.high(self.In[k])
                        else:
                            gpio.low(self.In[k])
                    sleep(delay)
    
    #funzioni che definiscono vari tipi di rotazione in base ai passi o agli angoli
    def clockwise_half_rotation(self,delay=STD_DELAY):
        self.rotation(CLOCKWISE,int(TOTAL_STEPS/2),delay)

    def anticlockwise_half_rotation(self,delay=STD_DELAY):
        self.rotation(ANTICLOCKWISE,int(TOTAL_STEPS/2),delay)

    def both_half_rotation(self,delay=STD_DELAY):
        self.clockwise_half_rotation(delay)
        self.anticlockwise_half_rotation(delay)
    
    def clockwise_full_rotation(self,delay=STD_DELAY):
        self.rotation(CLOCKWISE,TOTAL_STEPS,delay)

    def anticlockwise_full_rotation(self,delay=STD_DELAY):
        self.rotation(ANTICLOCKWISE,TOTAL_STEPS,delay)

    def both_full_rotation(self,delay=STD_DELAY):
        self.clockwise_full_rotation(delay)
        self.anticlockwise_full_rotation(delay)

    def clockwise_angle_rotation(self,angle,delay=STD_DELAY):
        steps=int((TOTAL_STEPS*angle)/360)#conversione gradi in passi
        self.rotation(CLOCKWISE,steps,delay)

    def anticlockwise_angle_rotation(self,angle,delay=STD_DELAY):
        steps=int((TOTAL_STEPS*angle)/360)#conversione gradi in passi
        self.rotation(ANTICLOCKWISE,steps,delay)

    def both_angle_rotation(self,angle,delay=STD_DELAY):
        self.clockwise_angle_rotation(angle,delay)
        self.anticlockwise_angle_rotation(angle,delay)

    def start_thread(self):#avvio il thread
            lock.acquire()
            self.fine=False
            self.parti=False
            lock.release()
            thread(stepper_thread, (self) )

    def start_moving(self, angle, delay=STD_DELAY):#avvio il movimento
        lock.acquire()
        self.angolo=angle
        self.parti=True
        self.delay=delay
        lock.release()

    def stop_moving(self):#fermo il movimento
        lock.acquire()
        self.parti=False
        lock.release()


    def end_thread(self):#uccido il thread
        lock.acquire()
        self.fine=True
        lock.release()
 