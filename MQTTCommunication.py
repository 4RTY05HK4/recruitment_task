import asyncio

from gmqtt import Client

from MQTT_info import MQTTInfo


class MQTTcallbacks:
    messages = asyncio.Queue(maxsize=1)

    def on_connect(self, client, flags, rc, properties):
        print("Connected")

    async def on_message(self, client, topic, payload, qos, properties):
        await self.messages.put(payload)

    def on_disconnect(self, client, packet, exc=None):
        print("Disconnected")


class MQTTCommunication:
    client = Client(MQTTInfo["login"])
    callbacks = MQTTcallbacks()
    client.on_connect = callbacks.on_connect
    client.on_message = callbacks.on_message
    client.on_disconnect = callbacks.on_disconnect

    async def connect(self):
        self.client.set_auth_credentials(MQTTInfo["login"], MQTTInfo["passwd"])
        await self.client.connect(MQTTInfo["IP"], MQTTInfo["port"])

    async def subToNode(self, topic):
        self.client.subscribe(topic)
        message = await self.callbacks.messages.get()
        return message

    async def subToStream(self, topic, message_count):
        self.client.subscribe(topic)
        msg_count = 0
        while msg_count < message_count:
            message = await self.callbacks.messages.get()
            print(message)
            msg_count += 1

    async def publishSet(self, topic, parameter):
        self.client.publish(topic, parameter)
        message = await self.callbacks.messages.get()
        return message

    async def publishGet(self, topic):
        self.client.publish(topic)
        message = await self.callbacks.messages.get()
        return message
