import pytest
import pytest_asyncio

from MQTTCommunication import MQTTCommunication


class TestClass:

    
    listOfNodesWithIds = ["cascade/4283","nexus/6267"]

    @pytest_asyncio.fixture(scope="session")
    async def connection(self):
        session = MQTTCommunication()
        await session.connect()
        yield session
        await session.client.disconnect()

    @pytest.mark.parametrize("nodeAndId",listOfNodesWithIds)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_sub_to_state(self, connection, nodeAndId):
        message = await connection.subToNode(f"{nodeAndId}/state/#")
        assert message.decode() == "true"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_unit_Kelvin(self, connection):
        await connection.subToNode(f"{self.nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{self.nodeAndId}/set/temperature/unit", "Kelvin"
        )
        assert message.decode() == "Kelvin"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_unit_Celcius(self, connection):
        await connection.subToNode(f"{self.nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{self.nodeAndId}/set/temperature/unit", "Celcius"
        )
        assert message.decode() == "Celcius"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_unit_Fahrenheit(self, connection):
        await connection.subToNode(f"{self.nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{self.nodeAndId}/set/temperature/unit", "Fahrenheit"
        )
        assert message.decode() == "Fahrenheit"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_sample_rate_to_0(self, connection):
        await connection.subToNode(f"{self.nodeAndId}/state/#")
        message = await connection.publishSet(f"{self.nodeAndId}/set/temperature/sample_rate", 0)
        assert int(message.decode()) == 0

    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_get_average(self, connection):
        await connection.subToNode(f"{self.nodeAndId}/state/#")
        await connection.publishSet(f"{self.nodeAndId}/set/temperature/unit", "Kelvin")
        temperatureInKelvin = await connection.publishGet(f"{self.nodeAndId}/get/temperature/average")
        await connection.publishSet(f"{self.nodeAndId}/set/temperature/unit", "Celcius")
        temperatureInCelcius = await connection.publishGet(f"{self.nodeAndId}/get/temperature/average")
        await connection.publishSet(f"{self.nodeAndId}/set/temperature/unit", "Fahrenheit")
        temperatureInFahrenheit = await connection.publishGet(f"{self.nodeAndId}/get/temperature/average")
        assert float(temperatureInCelcius.decode()) == 19.93
        assert float(temperatureInFahrenheit.decode()) == 67.87
        assert float(temperatureInKelvin.decode()) == 293.08


