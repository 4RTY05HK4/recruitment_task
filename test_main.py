import json

import pytest
import pytest_asyncio

from MQTTCommunication import MQTTCommunication
from nodes import listOfAverages, listOfNodesWithIds


class TestClass:
    listOfNodesWithIds = listOfNodesWithIds
    
    @pytest_asyncio.fixture(scope="session")
    async def connection(self):
        session = MQTTCommunication()
        await session.connect()
        yield session
        await session.client.disconnect()

    @pytest.mark.parametrize("nodeAndId", listOfNodesWithIds)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_sub_to_state(self, connection, nodeAndId):
        message = await connection.subToNode(f"{nodeAndId}/state/#")
        assert json.loads(message.decode()) == True

    @pytest.mark.parametrize("nodeAndId", listOfNodesWithIds)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_unit_Kelvin(self, connection, nodeAndId):
        await connection.subToNode(f"{nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{nodeAndId}/set/temperature/unit", "Kelvin"
        )
        assert message.decode() == 'Kelvin'

    @pytest.mark.parametrize("nodeAndId", listOfNodesWithIds)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_unit_Celcius(self, connection, nodeAndId):
        await connection.subToNode(f"{nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{nodeAndId}/set/temperature/unit", "Celcius"
        )
        assert message.decode() == 'Celcius'

    @pytest.mark.parametrize("nodeAndId", listOfNodesWithIds)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_unit_Fahrenheit(self, connection, nodeAndId):
        await connection.subToNode(f"{nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{nodeAndId}/set/temperature/unit", "Fahrenheit"
        )
        assert message.decode() == 'Fahrenheit'

    @pytest.mark.parametrize("nodeAndId", listOfNodesWithIds)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_set_sample_rate_to_0(self, connection, nodeAndId):
        await connection.subToNode(f"{nodeAndId}/state/#")
        message = await connection.publishSet(
            f"{nodeAndId}/set/temperature/sample_rate", 0
        )
        assert json.loads(message.decode()) == 0

    @pytest.mark.parametrize(
            "nodeAndId, expectedAverageInK, expectedAverageInC, expectedAverageInF", 
            listOfAverages)
    @pytest.mark.asyncio(loop_scope="session")
    async def test_pub_get_average(self, connection, nodeAndId, expectedAverageInK, expectedAverageInC, expectedAverageInF):
        await connection.subToNode(f"{nodeAndId}/state/#")
        await connection.publishSet(f"{nodeAndId}/set/temperature/unit", "Kelvin")
        temperatureInKelvin = await connection.publishGet(
            f"{nodeAndId}/get/temperature/average"
        )
        await connection.publishSet(f"{nodeAndId}/set/temperature/unit", "Celcius")
        temperatureInCelcius = await connection.publishGet(
            f"{nodeAndId}/get/temperature/average"
        )
        await connection.publishSet(
            f"{nodeAndId}/set/temperature/unit", "Fahrenheit"
        )
        temperatureInFahrenheit = await connection.publishGet(
            f"{nodeAndId}/get/temperature/average"
        )
        assert float(temperatureInCelcius.decode()) == expectedAverageInC
        assert float(temperatureInFahrenheit.decode()) == expectedAverageInF
        assert float(temperatureInKelvin.decode()) == expectedAverageInK
