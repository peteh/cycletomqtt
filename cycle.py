import asyncio
import logging
import paho.mqtt.client as mqtt
import json
import threading
import time
import wave
import io
import time
from threading import Thread

from bleak import BleakClient

from pycycling.cycling_power_service import CyclingPowerService

# TODO: generate from MAC
TRAINER_UNIQUE_ID = "taxc"
TRAINER_NAME = "Taxc"

# sensors: energy, rpm
async def run(address):
    async with BleakClient(address) as client:
        def my_measurement_handler(data):
            print(data)

        await client.is_connected()
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(my_measurement_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(30.0)
        await trainer.disable_cycling_power_measurement_notifications()

class Trainer():
    def __init__(self, ) -> None:
         pass
def _publishConfigTrainer(self):
        config = {}
        sensor = "power"
        topic = "homeassistant/sensor/%s/%s/config" % (TRAINER_UNIQUE_ID, sensor)
        config["~"] = "%s" % (TRAINER_UNIQUE_ID)
        config["availability_topic"] = "~"
        config["name"] = TRAINER_NAME + "Tacx"
        config["unique_id"] = "%s-%s" % (TRAINER_UNIQUE_ID, sensor)
        config["device_class"] = "power"
        #config["command_topic"] = "~/cmd"
        config["state_topic"] = "~/power"
        config["supported_features"] = ["start", "stop", "return_home", "pause", "status", "locate"]
        logging.info("Publishing homeassistant config for vacuum on %s", topic)
        self._client.publish(topic, json.dumps(config), retain=True)
        self._client.publish(TRAINER_UNIQUE_ID, "online")





class TrainerMqtt(object):
    def __init__(self):
        self._msgThread = threading.Thread(target = self._run)
        self._mqtt_client = mqtt.Client()
        self._mqtt_client.on_connect = self._onConnect
        self._mqtt_client.on_message = self._onMessage
        
    def _onConnect(self, client, userdata, flags, rc):
        # subscribe to all messages
        client.subscribe("hermes/intent/async:Shutup")
        client.subscribe("hermes/intent/async:StartListening")	
    
    def start(self):
        self._mqtt_client.connect('localhost', 1883)
        self._msgThread.start()
    
    def _run(self):
        self._mqtt_client.loop_forever()
        print("Ended Skill")
        
    def stop(self):
        print("Skill should end")
        self._mqtt_client.disconnect()
        print("mqtt disconnected")
        
    def _onMessage(self, client, userdata, msg):
        pass


    def publishData(self, data):
        self._mqtt_client.publish("test", "test")

  
if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    #device_address = "EAAA3D1F-6760-4D77-961E-8DDAC1CC9AED"
    device_address = "C1:BE:96:E5:B2:44"
    loop = asyncio.get_running_loop()
    loop.run_forever(run(device_address))

    skill = TrainerMqtt()
    skill.start()
    while(True):
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break;
    skill.stop()
