import gpio
import time
import threading
import pwm

ALLARM_PERIOD=1000
ALLARM_PULSE=500
ALLARM=0

DANGER_PERIOD=200
DANGER_PULSE=100
DANGER=1

CUSTOM=2
NOTHING=3

lock = threading.Lock()



def buzzer_thread(buz):#funzione nel thread
    while buz.fine==False:
        if buz.enable==True and buz.is_playing()==False:
            if(buz.sound_type==ALLARM):
                buz.allarm_ring()
            elif(buz.sound_type==DANGER):
                buz.danger_ring()
            else:
                buz.ring(buz.period, buz.pulse,buz.time_unit)
        else:
            sleep(2053)


class ACTIVE_BUZZER():
    def __init__(self,pin):#inizializzo la classe
        self.pin=pin
        gpio.mode(pin, OUTPUT)
        self.playing=False

        self.enable=False
        self.fine=False
        self.sound_type=NOTHING
        self.period=0
        self.pulse=0
        self.time_unit=MILLIS

    def ring(self, period, pulse,time_unit=MILLIS):#faccio suonare il buzzer
        pwm.write(self.pin, period, pulse,time_unit)
        self.playing=True


    def stop_ring(self):#fermo il buzzer
        self.ring(1000,0)
        self.playing=False

    def allarm_ring(self):#attivo suono di allarme
        self.ring(ALLARM_PERIOD,ALLARM_PULSE)

    def danger_ring(self):#attivo suono di pericolo
        self.ring(DANGER_PERIOD, DANGER_PULSE)

    def is_playing(self):#mi dice se sta suonando
        return self.playing

    def get_sound_type(self):#mi dice che cosa sta suonando
        return self.sound_type

    def set_sound(self, sound_type=ALLARM, period=0, pulse=0, time_unit=MILLIS):#decido che suono far suonare
        lock.acquire()
        self.sound_type=sound_type
        self.playing=False
        if(self.sound_type==CUSTOM):
            self.period=period
            self.pulse=pulse
            self.time_unit=time_unit
        lock.release()

    def start_thread(self):#avvio il thread
            lock.acquire()
            self.fine=False
            self.enable=False
            lock.release()
            thread(buzzer_thread, (self) )


    def start_sounding(self):#inizia a suonare
        lock.acquire()
        self.enable=True
        lock.release()

    def stop_sounding(self):#smette di suonare
        lock.acquire()
        self.enable=False
        self.sound_type=NOTHING
        self.stop_ring()
        lock.release()


    def end_thread(self):#uccido il thread
        lock.acquire()
        self.fine=True
        lock.release()

    
