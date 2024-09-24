import PERIFERICALS
from networking import wifi
from protocols import mqtt
import time
import credentials

#definisco i subscribers:
subs = [
    "SafetyReceive",
    "CareReceive"
]
#inizializzo i vari dispositivi:
device=PERIFERICALS.perifericals()
device.start_house_care()

#definisco la funzione per attivare/disattivare il controllo di sicurezza della casa tramite l'rfid:
def safety():
    while True:
        if(device.check_rfid_status() and device.is_changed_rfid_status()==True):
            device.start_house_safety()
        elif(device.rfid.changed==True):
            device.stop_house_safety()
        sleep(100)
#insierisco la funzione in un thread:
thread(safety)
#definisco la funzione che riceve il topic ed il messaggio e lo gestisce:    
def callback(client,topic,message):
    if(topic=="SafetyReceive"):
        if(message=="true" and not(device.get_safety())):
            device.rfid.allarm=True
            device.start_house_safety()
        elif(message=="false" and device.get_safety()):
            device.rfid.allarm=False
            device.stop_house_safety()
    elif(topic=="CareReceive"):
        if(message=="true" and not(device.get_care())):
            device.start_house_care()
        elif(message=="false" and device.get_care()):
            device.stop_house_care()
#funzione che controlla la sottoscrizione
def run():
    try:
        client.loop()
    except Exception as e:
        print("run thread exec",e)
        sleep(6000)

try:
    #configurazione e connessione al wifi
    wifi.configure(ssid = credentials.WIFI_SSID, password= credentials.WIFI_PASS)
    wifi.start()
    print(wifi.info())

    #connessione al server MQTT
    client = mqtt.MQTT("test.mosquitto.org","Gruppo53")
    for sub in subs:
        print("Subscribing to ",sub,client.on(sub,callback,1))
    client.connect()
    
    #metto la funzione run in un thread
    thread(run)
#eccezioni che subentrano in caso di errori
except WifiBadPassword:
    print("Bad Password")
except WifiBadSSID:
    print("Bad SSID")
except WifiException:
    print("Generic Wifi Exception")
except Exception as e:
    raise e


while True:
    #controllo se bisogna eseguire un controllo della qualità dell'aria/sicurezza
    if(device.get_care()):
        device.house_care()
    if(device.get_safety()):
        device.house_safety()
    #controllo se il dispositivo è connesso alla rete, se no aspetta che si riconnetta
    counter=0
   
    #publico le informazioni della ZM1 ai vari topic
    try:
        if(device.get_safety()):
            client.publish("Safety", "Safety System Attivato", qos=2, retain=False)
        else:
            client.publish("Safety", "Safety System Disattivato", qos=2, retain=False)

        if(device.get_care()):
            client.publish("Care", "Care System Attivato", qos=2, retain=False)
        else:
            client.publish("Care", "Care System Disattivato", qos=2, retain=False)

        if(device.get_care()):
            if(device.dc_motor.is_moving()):
                client.publish("Fan", str(int(device.dc_motor.get_speed())), qos=2, retain=False)
                client.publish("Pel", str(round(device.get_PEL(),2)), qos=2, retain=False)
            else:
                client.publish("Fan","0", qos=2, retain=False)
        else:
            client.publish("Fan","0", qos=2, retain=False)
            client.publish("Pel","0", qos=2, retain=False)

        if(device.get_care_allarm()):
            client.publish("Gas", "WARNING:High gas level", qos=2, retain=False)
        if(device.get_safety_allarm()):
            client.publish("Intruder", "INTRUSO", qos=2, retain=False)   
            
             
    except Exception as e:
        print(e)

    sleep(2000)