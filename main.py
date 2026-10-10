import asyncio
from gmqtt import Client

from MQTT_info import MQTTInfo


def on_connect(client, flags, rc, properties):
    print("Connected")


def on_message(client, topic, payload, qos, properties):
    print("RECV MSG:", payload.decode(), "on topic:", topic)


def on_disconnect(client, packet, exc=None):
    print("Disconnected")


def on_subscribe(client, mid, qos, properties):
    print("SUBSCRIBED")


async def main(MQTTInfo):
    client = Client("satelite")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    client.set_auth_credentials(MQTTInfo["login"], MQTTInfo["passwd"])
    await client.connect(MQTTInfo["IP"], MQTTInfo["port"])

    client.subscribe("cascade/4283/state/#")
    client.publish("cascade/4283/get/name")
    client.publish("cascade/4283/get/active")

    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main(MQTTInfo))
    except KeyboardInterrupt:
        print("Received exit signal, shutting down...")
