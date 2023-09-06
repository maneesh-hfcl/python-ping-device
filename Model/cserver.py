
class CServer:
    def __init__(self, ipAdd):
        ip, port = self.getIpPort(ipAdd) 
        self.ipAddress = ip
        self.port = port
        self.status = ""
        self.lastStatus = ""
        self.datetime = ""
        self.info = ""
    
    def updateStatus(self, value):
        self.lastStatus = value

    def getIpPort(self, ipadd):
        ip = ipadd if len(ipadd.split(':')) < 1 else ipadd.split(':')[0] 
        port = "" if len(ipadd.split(':')) < 1 else ipadd.split(':')[1]  
        return (ip, port)
    
    def getIPAddressPort(self):
        return self.ipAddress + ":" + self.port