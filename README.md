# Recruitment task
## 1 Description
A sensor network streaming measurements to MQTT server needs functional tests. As MQTT does not support standard request and response communication, it is provided on application level. Set and get operations can be achieved by publishing to corresponding topic ie.:
```
SUB node/id/state/#
PUB node/id/get/name
PUB node/id/set/temperature/unit
```
Tests will be written in Python, test specification is available in both .MD and .docx and test report will be generated in .html via pytest plugin or built-in pytest xml generator, specified at test launching.

## 2 Code
### 2.1 MQTT communication
Communication with MQTT server was implemented with gmqtt library, because it natively supports asynchronous communication. To handle messages coming from the server, callback methods had to be implemented. Messages are handled by on_message method and saved in asyncio queue. 
```
class MQTT_callbacks:
	 messages = asyncio.Queue()

	def on_connect(self, client, flags, rc, properties):
		print("Connected")

	async def on_message(self, client, topic, payload, qos, properties):
		await self.messages.put(payload)

	def on_disconnect(self, client, packet, exc=None):
		print("Disconnected")

```
To communicate with server a **gmqtt.Client** was set up with server credentials in class **MQTTCommunication**. Server credentials were saved in **MQTT_info.py** as a dictionary variable **MQTTinfo**. This file needs to be created in project root directory with exactly the same structure and name, for the communication with the server to be established. **MQTTCommunication** class extends **gmqtt.Client.publish()** and **.subscribe()** methods to simplify communication and read/write process. 

**MQTTCommunication** implements custom methods to handle subscribing and publishing to topics as well as handling returning messages. 

`def SubToNode(self, topic)` is used to subscribe to topic. It returns received response which is a single message.

`def SubToStream(self, topic, message_count)` is used to subscribe to stream on topic. It periodically prints messages. The amount of received messages is set by message_count. 

`def publishSet(self, topic, parameter)` is used to write parameter to topic, i.e. set unit to Celcius.

`def publishGet(self, topic)` is used to read data from topic, i.e. get average temperature.

### 2.2 Tests
Tests were based on written test specification. They were written in pytest with pytest_asyncio and pytest-html plugins. Because the communication with MQTT server is asynchronous, tests also had to be asynchronous, hence the need to encapsulate them in class and providing them with fixture containing connection to server. This had to be done this way, because all nodes present on server had to be tested and creating a new connection for each test, for each node is very bad practise. The fixture connection exist during testing session and is disposed of afterwards. For that it was marked with **@pytest_asyncio.fixture(scope=”session”)** Every test using that connection needs to be marked with **@pytest.mark.asyncio(loop_scope=”session”)**. Because of the requirement for all nodes to be tested, tests were parametrized. This was done by marking all tests with **@pytest.mark.paramtetrize(parameter, parameters_list)**. Report generation is done with either pytest-html plugin or built in report generator. Depending on which argument is used when running pytest:
`--html=Test_Report.html --self-contained-html`
or
`--junit-xml="Test_Report.xml"`

## 3 Setup & running
Project requires Python 3.14+ and pip to run. Clone the repository and run:

`pip install requirements.txt`

To connect with server a file MQTT_info.py has to be created at project root directory. It should contain a dict variable as shown below. The elements should be configured with proper credentials. That file is not shared in repository on purpose.
```
MQTTInfo = {
	"IP": "",
	"port": ,
	"login": "",
	"passwd": "",
}
```

To run tests open terminal in project root directory and run:

`python -m pytest --html=Test_Report.html --self-contained-html`

or

`python -m pytest --junit-xml="Test_Report.xml"`

depending if the test report should be generated in HTML or XML. Report will be generated in project root directory.

## 4 To do
```
- remaining tests with parametrization
- edge case coverage
- stream handling
```