import gpio
import time
import pwm
import BUZZER
import DC_MOTOR
import STEPPER
import ULTRASOUND
#import DHT11 #non è stato utilizzato poichè crea conflitti con gli altri dispositvi
import MQ_2
import VIBRATION_SWITCH
import RFID
import LCD
import RGB

ACTIVE=True
DISACTIVE=False
class perifericals:
    def __init__(self):#inizializzo la classe
        
        #set dati wifi e connessione

        #----
        self.lcd=LCD.GJD1602A_IIC()
        self.lcd.clear_line(0)
        self.lcd.puts("Caricamento...",y=0)

        self.rfid=RFID.MFRC522(D14, D13, D12, D27, D15)
        self.rfid.set_id(0x638763a2)
        self.rfid.start_thread()
        self.rfid.start_research()

        self.buzzer=BUZZER.ACTIVE_BUZZER(D23)
        self.buzzer.start_thread()

        self.mq2=MQ_2.MQ2(D35)
        self.mq2.set_limit(gas_limit=3500)
        self.mq2.start_thread()

        self.dc_motor=DC_MOTOR.L293D(D22, D2, D0)
        self.dc_motor.set_rotation(DC_MOTOR.CLW)

        self.stepper=STEPPER.motor(D5,D18,D19,D21)
        self.stepper.start_thread()

        self.usound=ULTRASOUND.HC_SR04(D10,D39)
        self.usound.set_limit(dist_limit=20)
        self.usound.start_thread()

        self.vib=VIBRATION_SWITCH.VIBRATION(D4)

        self.led=RGB.ledRGB(D33, D25, D26)
        self.led.blue()
        self.led.start_thread()

        self.care_active=False
        self.safety_active=False

        self.care_allarm_active=False
        self.safety_allarm_active=False

        #sleep(30000) #serve per scaldare
        self.lcd.puts("Sistema Attivo!",y=0)
        sleep(2000)
        self.lcd.clear()
        self.lcd.puts("Care Disattivo",y=0)
        self.lcd.puts("Safety Disattivo",y=1)

    def check_rfid_status(self):#vedo se lo stato del sistema di allarme deve essere attivo o disattivo
        return self.rfid.get_allarm_status()

    def start_house_care(self):#avvio sistema cura della casa
        self.lcd.clear_line(0)
        self.lcd.puts("Care Attivo",y=0)
        self.mq2.start_measuring()
        if(self.rfid.get_allarm_status()==RFID.DISACTIVE):
            self.led.green()
        self.care_active=True

    def stop_house_care(self):#disattivo sistema cura della casa
        self.care_active=False
        self.care_allarm_active=False
        self.lcd.clear_line(0)
        self.lcd.puts("Care Disattivo",y=0)
        self.mq2.stop_measuring()
        if(self.rfid.get_allarm_status()==RFID.DISACTIVE):
            self.led.blue()
        if(self.buzzer.get_sound_type()==BUZZER.ALLARM):
            self.led.stop_blinking()
            self.buzzer.stop_sounding()
        if(self.safety_active and not(self.safety_allarm_active)):
            self.led.yellow()
        elif(self.safety_allarm_active):
            self.led.red()
        self.dc_motor.stop()
        

    def house_care(self):#controllo del distema di cura della casa
        check=self.mq2.check_gas()
        if(check==MQ_2.OVER_LIMIT):
            self.care_allarm_active=True
            self.lcd.clear_line(0)
            self.lcd.puts("Aria contaminata",y=0)
            speed=int((10/319)*self.mq2.get_gas()-(9050/319))#equazione retta calcolata
            self.dc_motor.set_and_start(speed)
            if(self.buzzer.get_sound_type()!=BUZZER.DANGER and self.buzzer.get_sound_type()!=BUZZER.ALLARM):
                self.buzzer.set_sound(BUZZER.ALLARM)
                self.buzzer.start_sounding()
                self.led.magenta()
                self.led.start_blinking()
        elif(check==MQ_2.UNDER_LIMIT and self.dc_motor.is_moving()):
            self.care_allarm_active=False
            self.lcd.clear_line(0)
            self.lcd.puts("Care Attivo",y=0)
            self.dc_motor.stop()
            if(self.buzzer.get_sound_type()==BUZZER.ALLARM):
                self.buzzer.stop_sounding()
                self.led.stop_blinking()
                if(self.rfid.get_allarm_status()==RFID.DISACTIVE):
                    self.led.green()
                else:
                    self.led.yellow()

    def start_house_safety(self):#avvio sistema di sicurezza della casa
        self.lcd.clear_line(1)
        self.lcd.puts("Safety Attivo",y=1)
        self.vib.start()
        self.usound.start_measuring()
        self.stepper.start_moving(angle=30,delay=STEPPER.STD_DELAY*10)
        if(not(self.led.is_blinking()) and not(self.buzzer.get_sound_type()==BUZZER.ALLARM)):
            self.led.yellow()
        sleep(2000)
        self.safety_active=True

    def stop_house_safety(self):#disattivo sistema di sicurezza della casa
        self.safety_active=False
        self.safety_allarm_active=False
        self.lcd.clear_line(1)
        self.lcd.puts("Safety Disattivo",y=1)
        if(self.buzzer.get_sound_type()==BUZZER.DANGER):
            self.buzzer.stop_sounding()
            self.led.stop_blinking()
        if(self.care_allarm_active):
            self.led.magenta()
        elif(self.care_active==ACTIVE):
            self.led.green()
        else:
            self.led.blue()
        self.usound.stop_measuring()
        self.stepper.stop_moving()


    def house_safety(self):#controllo del sistema di sicurezza della casa
        vibration=self.vib.check_vibration()
        presence=self.usound.check_dist()
        if(vibration or presence):
            self.safety_allarm_active=True
            self.lcd.clear_line(1)
            self.lcd.puts("Intrusione!",y=1,x=3)
            if(self.buzzer.get_sound_type()!=BUZZER.DANGER):
                self.buzzer.set_sound(BUZZER.DANGER)
                self.buzzer.start_sounding()
                self.led.red()
                self.led.start_blinking()

    def get_PEL(self):#mi restituisce la PEL
        return self.mq2.get_PEL()

    def get_care(self):#mi dice se il sistema di cura della casa è attivo
        return self.care_active

    def get_safety(self):#mi dice se il sistema di sicurezza della casa è attivo
        return self.safety_active

    def get_care_allarm(self):#mi dice se vengono rilevati valori di fumo anomali
        return self.care_allarm_active

    def get_safety_allarm(self):#mi dice se è stata rilevata un'intrusione
        return self.safety_allarm_active

    def is_changed_rfid_status(self):#mi dice se lo stato dell'RFID è cambiato
        return self.rfid.is_changed()