import asyncio
import logging
import paho.mqtt.client as mqtt
import json

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

    def _publishConfigTrainer(self):
        config = {}
        sensor = "power"
        topic = "homeassistant/sensor/%s/%s/config" % (TRAINER_UNIQUE_ID, sensor)
        config["~"] = "%s/%s" % (TRAINER_UNIQUE_ID, sensor)
        config["availability_topic"] = "~"
        config["name"] = TRAINER_NAME + "Tacx"
        config["unique_id"] = "%s/%s" % (TRAINER_UNIQUE_ID, sensor)
        config["device_class"] = "power"
        #config["command_topic"] = "~/cmd"
        config["schema"] = "state"
        config["state_topic"] = "~/state"
        config["supported_features"] = ["start", "stop", "return_home", "pause", "status", "locate"]
        logging.info("Publishing homeassistant config for vacuum on %s", topic)
        self._client.publish(topic, json.dumps(config), retain=True)
        self._client.publish(TRAINER_UNIQUE_ID, "online")

if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    #device_address = "EAAA3D1F-6760-4D77-961E-8DDAC1CC9AED"
    device_address = "C1:BE:96:E5:B2:44"
    loop = asyncio.get_event_loop()
    loop.run_forever(run(device_address))


    