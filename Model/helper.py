from Model.ping_from_db import getPingFrmDB
from Model.db import GetDevice, GetDBConfiguration, GetDBInfo,SaveDBConfiguration

def GetDBDevice():
    lstNVR, lstCam = GetDevice()
    return (lstNVR + lstCam)

def GetPingFromDBDevice(q):
    lstDevices = GetDBDevice()
    getPingFrmDB(q, lstDevices)

def GetDBConfig():
    return GetDBConfiguration()

def hlpr_GetDBInfo():
    return GetDBInfo()

def hlpr_SaveDBConfig(server, username, password, dbname):
    return SaveDBConfiguration(server, username, password, dbname)
