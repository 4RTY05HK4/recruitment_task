# Introduction
We have developed a distributed sensor network generating a continuous stream of measurements published to an MQTT broker.  Connection to MQTT broker can be established at an IP address shared in a message from a recruiter at port 32760. When establishing a connection, client must authorize using a client id, which was also shared. TLS and client-side certificates are not required.
Each node publishes a persistent topic to __\<node>/\<id>/state/active__ that can be used to inspect available nodes.
Each sensor may also be configured remotely using the same communication medium.  
As MQTT is not designed for a request-response model, this functionality is provided on an application level.
set operation for write or execute access (__\<node>/\<id>/set/\<parameter_path>__).
get operation for read access (__\<node>/\<id>/get/\<parameter_path>__).
state endpoints for value change notifications (__\<node>/\<id>/state/\<parameter_path>__).
Access to non-existent parameter does not yield a response.  Setting a parameter generates a state notification with its current value. Out of range values should be discarded. Once enabled, the measurements are streamed to __\<node>/\<id>/stream/\<sensor_type>__ topics periodically.

**Read example**  

SUB variant_a/12/state/#  
-> PUB variant_a/12/get/name  
<- PUB variant_a/12/state/name 'Bill'  

**Write example - enable streaming**  

SUB variant_a/12/state/#  
SUB variant_a/12/stream/#  
-> PUB variant_a/12/set/temperature/sample_rate 2  
<- PUB variant_a/12/state/temperature/sample_rate 2  
<- PUB variant_a/12/stream/temperature "35.6"  
<- PUB variant_a/12/stream/temperature "35.6"  
<- PUB variant_a/12/stream/temperature "35.8"  

# Goal

Your goal is to prepare a test specification, a suite of automated functional tests implemented in Python, and a test report.
Warning Each node implements the same API and functionality, but runs slightly different software. Every node must be tested.

# Device documentation

## Measurement streams

Device supports three measurement streams. Updates are sent periodically with a frequency configured through associated 'sample_rate' parameter.

| Name  | Data format | Description |
|-------|-------------|-------------|
| temperature	| String with floating point number | Temperature in Celcius/Fahrenheit/Kelvin.  |
| pressure	| Binary: 	                            | Pressure in Pa/Bar/psi. | 
|           | Timestamp: uint32_t                   | Measurements include a UNIX timestamp. |
|           | Pressure: float32                     | All values are little-endian           |
| orientation | JSON:                               | Node orientation (Euler angles). |
|             | timestamp: uint32_t                 | Measurements include a UNIX timestamp and accuraccy. |
|             | yaw: float                          |  |
|             | pitch: float                        |  |
|             | roll: float                         |  |
|             | accuracy: float                     |  |


## Configuration

**All parameters are encoded as text strings.**
 
| Name | Access | Data format | Range | Description |
|------|--------|-------------|-------|-------------|
| name |	R |	String | 5-16 alphanumeric characters	| Name of the device. |
| temperature/sample_rate | RW | Integer | 0-5	| Temperature sensor sampling rate in seconds. Send 0 to disable the measurement stream. |
| temperature/unit |	RW | String | Celcius/Fahrenheit/Kelvin |	Unit used by the temperature measurement stream. |
| temperature/average |	R | String | Celcius/Fahrenheit/Kelvin |	The average temperature, can be treated as constant. |
| pressure/sample_rate | RW | Integer | 0-50 | Temperature sensor sampling rate in seconds. Send 0 to disable the measurement stream. |
| pressure/unit | RW | String | Pa/Bar/psi | Unit used by the pressure measurement stream |
| pressure/average | R | float32 | Pa/Bar/psi | The average pressure, can be treated as constant. |
| orientation/sample_rate | RW | Integer | 0-100 | Orientation sensor sampling rate in seconds. Send 0 to disable the measurement stream. |
| orientation/unit | RW | String | deg/Rad | Unit used by the orientation measurement stream. |
| orientation/average | R | See orientation measurement stream | deg/Rad | The average pressure, can be treated as constant. |
| active | R | Boolean | false/true | Persistent message signifying the presence of node. |

