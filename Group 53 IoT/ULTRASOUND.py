import gpio
import time
import threading

ERR=-1
DELAY=1
STD_TIME=3000
MAX_DIST=350
OVER_LIMIT=True
UNDER_LIMIT=False
lock = threading.Lock()

def ultrasound_thread(sound):#funzione del thread
    while sound.fine==False:
        sleep(2309)
        while sound.misura==True:
            lock.acquire()
            sound.distanza=sound.calcola_distanza()
            lock.release()
            sleep(sound.time)


class HC_SR04:
    def __init__(self,trig,echo):#inizializzo la classe
        self.trig=trig
        self.echo=echo
        gpio.mode(self.trig, OUTPUT)
        gpio.mode(self.echo, INPUT)
        self.fine=False
        self.misura=False
        self.distanza=0
        self.time=STD_TIME
        self.dist_limit=MAX_DIST

    def calcola_distanza(self):#calcolo distanza misurata
        gpio.low(self.trig)
        sleep(200)
        gpio.high(self.trig)
        sleep(10)
        gpio.low(self.trig)
        check=time.time()
        end=0
        start=0
        while(gpio.get(self.echo)==0 and (time.time()-check)<1):
            start=time.time()
        while(gpio.get(self.echo)==1):
            end=time.time()
        elapsed_time=end-start
        distance=elapsed_time*17150
        if(distance<=400 and distance>=0):
            return distance
        else:
            return ERR

    def set_limit(self,dist_limit=MAX_DIST):#setto la distanza minima da non superare
        lock.acquire()
        self.dist_limit=dist_limit
        lock.release()

    def check_dist(self):#controllo se i limiti sono stati superati
        if(self.distanza<=self.dist_limit and not(self.distanza==ERR)):
            return OVER_LIMIT
        return UNDER_LIMIT

    def start_thread(self):#avvio il thread
            lock.acquire()
            self.fine=False
            self.misura=False
            lock.release()
            thread(ultrasound_thread, (self) )

    def start_measuring(self,time=STD_TIME):#avvio la misurazione
        lock.acquire()
        self.misura=True
        self.time=time
        lock.release()


    def stop_measuring(self):#fermo la misurazione
        lock.acquire()
        self.misura=False
        lock.release()


    def end_thread(self):#uccido il thread
        lock.acquire()
        self.fine=True
        lock.release()

    def get_distanza(self):#mi restituisce la distanza calcolata
        return self.distanza