import adc
import gpio
import time
import threading

lock = threading.Lock()

STD_TIME=3000
MAX_GAS=4095
OVER_LIMIT=True
UNDER_LIMIT=False
#temp, hum


def mq2_thread(mq2):#funzione nel thread
    while mq2.fine==False:
        if mq2.misura==True:
            while mq2.misura==True:
                lock.acquire()
                mq2.read()
                lock.release()
                sleep(mq2.time)
        else:
            sleep(2129)

class MQ2():
    def __init__(self,pin):#inizializzo la classe
        self.pin=pin
        gpio.mode(self.pin, INPUT_ANALOG)
        self.gas=0
        self.gas_limit=MAX_GAS
        self.fine=False
        self.misura=False
        self.time=STD_TIME

    def read(self):#leggo valore
        self.gas=adc.read(self.pin)
        

    def get_gas(self):#ritorna il valore rilevato
        print("Gas :",self.gas)
        return self.gas

    def get_PEL(self):#valori soglia di accettabilità gas tossici (maggiore di 1 è inaccettabile, sotto è ok)
        return (self.get_gas()/self.gas_limit)

    def set_limit(self,gas_limit=MAX_GAS):#definisco limiti
        lock.acquire()
        self.gas_limit=gas_limit
        lock.release()

    def check_gas(self):#controllo se i limiti sono rispettati
        if(self.gas>=self.gas_limit):
            return OVER_LIMIT
        return UNDER_LIMIT
        
    def start_thread(self):#avvio il thread
            lock.acquire()
            self.fine=False
            self.misura=False
            lock.release()
            thread(mq2_thread, (self) )

    def start_measuring(self,time=STD_TIME):#inizio misurazione
        lock.acquire()
        self.misura=True
        self.time=time
        lock.release()

    def stop_measuring(self):#ferma misurazione
        lock.acquire()
        self.misura=False
        lock.release()


    def end_thread(self):#uccido il thread
        lock.acquire()
        self.fine=True
        lock.release()
