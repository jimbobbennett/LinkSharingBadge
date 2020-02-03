import iotc, os
from iotc import IOTConnectType, IOTLogLevel
from dotenv import load_dotenv

load_dotenv()

deviceId = os.environ['DEVICE_ID']
scopeId = os.environ['SCOPE_ID']
deviceKey = os.environ['DEVICE_KEY']

iotc = iotc.Device(scopeId, deviceKey, deviceId, IOTConnectType.IOTC_CONNECT_SYMM_KEY)
iotc.setLogLevel(IOTLogLevel.IOTC_LOGGING_API_ONLY)

def onconnect(info):
    print("- [onconnect] => status:" + str(info.getStatusCode()))

def onmessagesent(info):
    print("\t- [onmessagesent] => " + str(info.getPayload()))

def oncommand(info):
    global gMode
    print("- [oncommand] => " + info.getTag() + " => " + str(info.getPayload()))

def onsettingsupdated(info):
    print("- [onsettingsupdated] => " + info.getTag() + " => " + info.getPayload())

iotc.on("ConnectionStatus", onconnect)
iotc.on("MessageSent", onmessagesent)
iotc.on("Command", oncommand)
iotc.on("SettingsUpdated", onsettingsupdated)

iotc.connect()

while iotc.isConnected():
    iotc.doNext() # do the async work needed to be done for MQTT