import gpio
import threading
    
STD_TIME=500
lock = threading.Lock()

def blink_thread(led):#funzione del thread
    while led.fine==False:
        sleep(2161)
        while led.lampeggia==True:
            lock.acquire()
            led.blink(led.time)
            lock.release()
    
    

class ledRGB:
    def __init__(self,pinR,pinG,pinB):#inizializzo la classe
        self.colore_settato=(0,0,0)
        self.lampeggia=False

        self.RGBcolor=(pinR,pinG,pinB)
        gpio.mode(pinR,OUTPUT)
        gpio.mode(pinG,OUTPUT)
        gpio.mode(pinB,OUTPUT)

        self.time=STD_TIME
        self.fine=False

    def color(self, R=0,G=0,B=0):#Ssetto il colore
        col = (R,G,B)
        for i in range(3):
            if(col[i]==0):
                gpio.set(self.RGBcolor[i],LOW)
            else:
                gpio.set(self.RGBcolor[i],HIGH)
            self.colore_settato=(R,G,B)
    #funzioni per settare il relativo colore
    def red(self):
        lock.acquire()
        self.color(0,1,1)
        lock.release()

    def green(self):
        lock.acquire()
        self.color(1,0,1)
        lock.release()

    def blue(self):
        lock.acquire()
        self.color(1,1,0)
        lock.release()

    def white(self):
        lock.acquire()
        self.color(0,0,0)
        lock.release()

    def magenta(self):
        lock.acquire()
        self.color(0,1,0)
        lock.release()

    def yellow(self):
        lock.acquire()
        self.color(0,0,1)
        lock.release()

    def turquoise(self):
        lock.acquire()
        self.color(1,0,0)
        lock.release()

    def turn_off(self):#spengo il led
        self.color(1,1,1)
    
    def blink(self,time=STD_TIME):#lampeggio led
        colore_salva=self.colore_settato
        self.turn_off()
        sleep(self.time)
        self.color(colore_salva[0],colore_salva[1],colore_salva[2])
        sleep(self.time)

    def start_thread(self):#avvio il thread
        lock.acquire()
        self.fine=False
        self.lampeggia=False
        lock.release()
        thread(blink_thread, (self) )

    def start_blinking(self,time=STD_TIME):#avvio lampeggio
        lock.acquire()
        self.lampeggia=True
        self.time=time
        lock.release()


    def stop_blinking(self):#fermo il lampeggio
        lock.acquire()
        self.lampeggia=False
        lock.release()



    def end_thread(self):#uccido il thread
        lock.acquire()
        self.fine=True
        lock.release()
        

    def is_blinking(self):#mi dice se il led sta lampeggiando
        return self.lampeggia