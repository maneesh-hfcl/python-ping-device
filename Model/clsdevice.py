class ClsDevice:
    def __init__(self, device):
        print(device)
        self.ipAddress = device["IP"]
        self.port = device["Port"]
        self.name = device["Name"]
        self.status = ""
        self.lastStatus = ""
        self.datetime = ""
        self.info = ""
        self.type = device["Type"]
    
    def updateStatus(self, value):
        self.lastStatus = value

    def getIpPort(self, ipadd):
        ip = ipadd if len(ipadd.split(':')) < 2 else ipadd.split(':')[0] 
        port = "" if len(ipadd.split(':')) < 2 else ipadd.split(':')[1]  
        return (ip, port)
    
    def getIPAddressPort(self):
        return self.ipAddress + ":" + self.port