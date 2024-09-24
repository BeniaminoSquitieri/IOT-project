from components.dht11 import dht11
import gpio
import time
import threading
import pwm

lock = threading.Lock()


STD_TIME=2000
MAX_TEMP=50
MIN_TEMP=0
MAX_HUM=90
MIN_HUM=20
OVER_LIMIT=True
UNDER_LIMIT=False


def dht11_thread(dht):
    while dht.fine==False:
        if(dht.misura==True):
            while dht.misura==True:
                lock.acquire()
                dht.read()
                lock.release()
                sleep(dht.time)
                sleep(2000)
        else:
            sleep(2081)


class DHT11():
    def __init__(self,pin):
        self.pin=pin
        self.hum=0
        self.temp=0
        self.hum_limit=MAX_HUM
        self.temp_limit=MAX_TEMP
        self.fine=False
        self.misura=False
        self.time=STD_TIME

    def read(self):
        self.hum,self.temp=dht11.read(self.pin)

    def get_hum(self):
        return self.hum

    def get_temp(self):
        return self.temp

    def set_limit(self,hum_limit=MAX_TEMP,temp_limit=MAX_HUM):
        lock.acquire()
        self.hum_limit=hum_limit
        self.temp_limit=temp_limit
        lock.release()

    def check_hum(self):
        if(self.hum>=self.hum_limit):
            return OVER_LIMIT
        return UNDER_LIMIT

    def check_temp(self):
        if(self.temp>=self.temp_limit):
            return OVER_LIMIT
        return UNDER_LIMIT
        
    def start_thread(self):
            lock.acquire()
            self.fine=False
            self.misura=False
            lock.release()
            thread(dht11_thread, (self) )

    def start_measuring(self,time=STD_TIME):
        lock.acquire()
        self.misura=True
        self.time=time
        lock.release()

    def stop_measuring(self):
        lock.acquire()
        self.misura=False
        lock.release()


    def end_thread(self):
        lock.acquire()
        self.fine=True
        lock.release()
