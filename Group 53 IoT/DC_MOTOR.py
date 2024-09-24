import gpio
import pwm
PERIOD=1000
CLW=True
ACLW=False

class L293D(): #versione che gestisce un solo motore, per usarne due, inizializzare questa classe due volte
    def __init__(self,enable,in1,in2):#inizializzo la classe
        self.enable=enable
        self.in1=in1
        self.in2=in2
        self.period=PERIOD
        self.pulse=0
        self.moving=False
        gpio.mode(self.in1, OUTPUT)
        gpio.low(self.in1)
        gpio.mode(self.in2, OUTPUT)
        gpio.low(self.in2)
        gpio.mode(self.enable, OUTPUT)

    def set_rotation(self,verse=CLW):#decido il verso di rotazione
        if(verse==CLW):
            gpio.low(self.in2)
            gpio.high(self.in1)
        elif(verse==ACLW):
            gpio.low(self.in1)
            gpio.high(self.in2)

    def set_speed(self,speed=0):#setto la velocità di rotazione
        if(speed>=0 and speed<=100):
            self.pulse=speed*10
        else:
            print("velocità inserita errata")
    def get_speed(self):
        return self.pulse/10

    def start(self):#avvio la rotazione
        pwm.write(self.enable, self.period, self.pulse,time_unit=MICROS)
        self.moving=True

    def set_and_start(self,speed=0):#setto la velocità di rotazione e avvio la rotazione
        if(speed>=0 and speed<=100):
            self.pulse=speed*10
            self.start()
        else:
            print("velocità inserita errata")
    
    def stop(self): #fermo la rotazione
        pwm.write(self.enable, self.period, 0,time_unit=MICROS)
        self.moving=False

    def is_moving(self):# mi dice se il sistema è in rotazione
        return self.moving