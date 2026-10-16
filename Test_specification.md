# Test specification

## Summary

Each sensor apart from broadcasting measurement data, broadcasts it's current state and name. Additionally, sensors in each node can be configured in some way. Therfore, tests should check measurements, device state and name as well as response to being configured.

## Details

### Tested node structure

node  
&emsp;|– id
&emsp;&emsp;&ensp;|– name
&emsp;&emsp;&ensp;|- state
&emsp;&emsp;&ensp;|- temperature
&emsp;&emsp;&ensp;|- pressure  
&emsp;&emsp;&ensp;|- orientation

---
### name & state

| Test description                                             | Expected result                           |
| ------------------------------------------------------------ | ----------------------------------------- |
| When name is requested then device returns it's name         | string type variable containg device name |
| When state of node is requested then node returns it's state | Boolean variable representing node status |

---
### temperature

| Test description                                                                    | Expected result                                                          |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| When unit is set then device should respond with new unit                           | String variable containing the set unit                                  |
| If unit is set then measurements should be received in set unit                     | Floating point value converted to set unit                               |
| If unit is set then average should be received in set unit                          | String variable containing floating point value converted to set unit    |
| When sample rate is set then device should respond with set sample rate             | Integer value equal to set sample rate                                   |
| If sample rate is set to 5 then device should stream a reading once every 5 seconds | Floating point value converted to set unit received once every 5 seconds |
| If sample rate is set to 4 then device should stream a reading once every 4 seconds | Floating point value converted to set unit received once every 4 seconds |
| If sample rate is set to 3 then device should stream a reading once every 3 seconds | Floating point value converted to set unit received once every 3 seconds |
| If sample rate is set to 2 then device should stream a reading once every 2 seconds | Floating point value converted to set unit received once every 2 seconds |
| If sample rate is set to 1 then device should stream a reading once every 1 seconds | Floating point value converted to set unit received once every 1 seconds |
| If sample rate is set to 0 then device should stop streaming readings               | No value should be received for a least 5 seconds                        |
| When average is requested then device should respond with average value in set unit | String variable containing floating point value in set unit              |

---
### pressure

| Test description                                                                      | Expected result                                                               |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| When unit is set then device should respond with new unit                             | String variable containing the set unit                                       |
| If unit is set then measurements should be received in set unit                       | Floating point value converted to set unit                                    |
| If unit is set then average should be received in set unit                            | Floating point variable containing floating point value converted to set unit |
| When sample rate is set then device should respond with set sample rate               | Integer value equal to set sample rate                                        |
| If sample rate is set to 50 then device should stream a reading once every 50 seconds | Floating point value converted to set unit received once every 50 seconds     |
| If sample rate is set to 10 then device should stream a reading once every 10 seconds | Floating point value converted to set unit received once every 10 seconds     |
| If sample rate is set to 2 then device should stream a reading once every 2 seconds   | Floating point value converted to set unit received once every 2 seconds      |
| If sample rate is set to 0 then device should stop streaming readings                 | No value should be received for a least 50 seconds                            |
| When average is requested then device should respond with average value in set unit   | Floating point variable containing constant floating point value in set unit  |

---
### orientation

| Test description                                                                        | Expected result                                                                                    |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| When unit is set then device should respond with new unit                               | String variable containing the set unit                                                            |
| If unit is set then measurements should be received in set unit                         | Floating point value converted to set unit                                                         |
| If unit is set then average should be received in set unit                              | Floating point variable containing floating point value converted to set unit                      |
| When sample rate is set then device should respond with set sample rate                 | Integer value equal to set sample rate                                                             |
| If sample rate is set to 100 then device should stream a reading once every 100 seconds | Floating point value converted to set unit received once every 100 seconds                         |
| If sample rate is set to 5 then device should stream a reading once every 5 seconds     | Floating point value converted to set unit received once every 5 seconds                           |
| If sample rate is set to 0 then device should stop streaming readings                   | No value should be received for a least 100 seconds                                                |
| When average is requested then device should respond with average value in set unit     | JSON containing timestamp and constant values describing yaw, pitch, roll and accuracy in set unit |