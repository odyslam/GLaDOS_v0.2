#   Copyright 2015 Eric Ptak - trouch.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from webiopi.decorators.rest import request, response
from webiopi.utils.types import toint
from webiopi.devices import instance

class AnalogSensor():
    def __init__(self, adc, channel):
        self.adcname = adc
        self.channel = toint(channel)
        self.adc = instance.deviceInstance(self.adcname)

    def __str__(self):
        return "AnalogSensor"
    
    def __family__(self):
        return "AnalogSensor"
    
    @request("GET", "integer")
    @response("%d")
    def read(self):
        return self.adc.analogRead(self.channel)
    
    @request("GET", "float")
    @response("%.2f")
    def readFloat(self):
        return self.adc.analogReadFloat(self.channel)
    
    @request("GET", "volt")
    @response("%.2f")
    def readVolt(self):
        return self.adc.analogReadVolt(self.channel)

class Photoresistor(AnalogSensor):
    def __init__(self, adc, channel):
        AnalogSensor.__init__(self, adc, channel)

    def __str__(self):
        return "Photoresistor"
    
class Thermistor(AnalogSensor):
    def __init__(self, adc, channel):
        AnalogSensor.__init__(self, adc, channel)

    def __str__(self):
        return "Thermistor"
    
class DistanceSensor(AnalogSensor):
    def __init__(self, adc, channel):
        AnalogSensor.__init__(self, adc, channel)

    def __str__(self):
        return "DistanceSensor"
    
class LoadSensor(AnalogSensor):
    def __init__(self, adc, channel):
        AnalogSensor.__init__(self, adc, channel)

    def __str__(self):
        return "LoadSensor"
    
    
    
class ServoMotor():
    def __init__(self, pwm, channel):
        self.pwm = instance.deviceInstance(pwm)
        self.pwmname = pwm
        self.channel = toint(channel)
        self.pwm.pwmWriteAngle(self.channel, 0)
        
        
    def __str__(self):
        return "ServoMotor"
    
    def __family__(self):
        return "ServoMotor"
    
    @request("GET", "angle")
    @response("%.2f")
    def readAngle(self):
        return self.pwm.pwmReadAngle(self.channel)
        
    @request("POST", "angle/%(value)f")
    @response("%.2f")
    def writeAngle(self, value):
        return self.pwm.pwmWriteAngle(self.channel, value)
    
class AnalogActuator():
    def __init__(self, pwm, channel):
        self.pwm = instance.deviceInstance(pwm)
        self.pwmname = pwm
        self.channel = toint(channel)
        
    def __str__(self):
        return "AnalogActuator"
    
    def __family__(self):
        return "AnalogActuator"
    
    @request("GET", "float")
    @response("%.2f")
    def readFloat(self):
        return self.pwm.pwmReadFloat(self.channel)
        
    @request("POST", "float/%(value)f")
    @response("%.2f")
    def writeFloat(self, value):
        return self.pwm.pwmWriteFloat(self.channel, value)

class LightDimmer(AnalogActuator):
    def __init__(self, pwm, channel):
        AnalogActuator.__init__(self, pwm, channel)

    def __str__(self):
        return "LightDimmer"
