import time
import i2c
import gpio


class GJD1602A_IIC():
    def __init__(self):#inizializzo la classe
        self.i2c=i2c.I2c(0x27)

        scan_result = i2c.scan()
        
        while not scan_result:
            print("Cannot Locate I2C Device")
            sleep(10)
            scan_result = i2c.scan()
        self.LCD_I2C_ADDR = i2c.scan()[0]
        self.bufs = []  # è una lista di bytes dove inserirò tette le informazioni
        self.BK = 0x08
        self.RS = 0x00
        self.E = 0x04
        #sequenza di "avvio"
        self.queue(0x30)  # 0011
        self.execute()
        sleep(5)
        self.queue(0x30)  # 0011
        self.execute()
        sleep(5)
        self.queue(0x20)  # 0010
        self.execute()
        sleep(5)
        self.add_command(0x28,run=True)  # 0010   1000
        self.on()
        self.add_command(0x06)  # 0000   0110
        self.add_command(0x01)  # 0000   0001
        self.execute()

    def queue(self, dat):#aggiungo i dati in una coda, aspettando l'esecuzione   
        dat = dat & 0xF0
        dat |= self.BK
        dat |= self.RS
        
        self.bufs.append(dat | 0x04) # abilito high
        self.bufs.append(dat) # abilito low
            
    def execute(self):#funzione che mi permette di eseguire un singolo comando
        try:
            bytearray_to_write = bytearray(len(self.bufs))
            for i in range(len(self.bufs)):
                bytearray_to_write[i] = self.bufs[i]
            self.i2c.write(bytearray_to_write)
            self.bufs=[]
            sleep(5)
        except Exception as e:
            print(e)

    def add_command(self, cmd, run=False):#aggiungo un comando
        self.RS = 0
        self.queue(cmd)
        self.queue(cmd << 4)
        if run:
            self.execute()

    def add_data(self, dat):#aggiungo dei dati
        self.RS = 1
        self.queue(dat)
        self.queue(dat << 4)

    def clear(self):#pulisco il display
        self.add_command(1,run=True)
    #funzioni di cortesia
    def backlight(self, on):
        if on:
            self.BK = 0x08
        else:
            self.BK = 0
        self.add_command(0,run=True)

    def on(self):
        self.add_command(0x0C,run=True)

    def off(self):
        self.add_command(0x08,run=True)

    def shl(self):
        self.add_command(0x18,run=True)

    def shr(self):
        self.add_command(0x1C,run=True)

    def char(self, ch, x=-1, y=0):#funzione che mi permette di aggiungere un carattere al buffer dei comandi
        if x >= 0:
            if y == 0:
                a = 0x80
            if y == 1:
                a = 0xC0
            if y == 2:
                a = 0x80 + 20
            if y == 3:
                a = 0xC0 + 20
            a += x
            self.add_command(a)
        self.add_data(ch)

    def puts(self, s, y=0, x=0):#scrivo sul display inserendo la stringa e la cordinata
        try:
            if len(s) > 0:
                self.char(ord(s[0]), x, y)
                for i in range(1, len(s)):
                    self.char(ord(s[i]))
        except Exception as e:
            print(e)
        self.execute()

    def clear_line(self,y=0):#pulisco una linea del display
        self.puts("                  ",y)