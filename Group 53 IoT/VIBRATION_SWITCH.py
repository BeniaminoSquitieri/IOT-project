import gpio


detected=False

def vib():#funzione chiamata da gpio.on_fall
    global detected
    detected=True
    

class VIBRATION():
    def __init__(self,pin):#inizializzo la classe
        self.pin=pin
        gpio.mode(self.pin,INPUT_PULLUP)
        gpio.on_fall(self.pin, vib, pull=INPUT_PULLUP)

    def start(self):#avvio la misurazione
        global detected
        detected=False

    def check_vibration(self):#controlla se ha rilevato una vibrazione
        global detected
        if(detected):
            detected=False
            return True
        else:
            return False