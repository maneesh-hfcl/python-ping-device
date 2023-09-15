import pymssql
import configparser

db_server = "" #"127.0.0.1"
db_user = "" #config['DBConnection']['db_user'] #"sa"
db_password = "" #config['DBConnection']['db_password'] #"qwerty@1"
db_database = "" #config['DBConnection']['db_database'] 
db_table_dev = "tDev"
db_table_nvr = "tNvr"

def GetDBInfo():
    return db_server,db_user,db_password,db_database


def GetDBConfiguration():
    config = configparser.ConfigParser()
    config.read("config.ini")
    print(config.read_file)
    global db_server, db_user, db_password, db_database
    db_server = config['DBConnection']['db_server'] #"127.0.0.1"
    db_user = config['DBConnection']['db_user'] #"sa"
    db_password = config['DBConnection']['db_password'] #"qwerty@1"
    db_database = config['DBConnection']['db_database'] 
    return (db_server, db_user, db_password, db_database)

def SaveDBConfiguration(server, username, password, dbname):
    try:
        global db_server, db_user, db_password, db_database
        config = configparser.ConfigParser()
        config['DBConnection'] = {
                                    'db_server' : server,
                                    'db_user' : username,
                                    'db_password' : password,
                                    'db_database' : dbname
                                }
                                
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        print("success db config")
        db_server = server
        db_user = username
        db_password = password
        db_database = dbname
        return "success"
    except:
        print("error db config save")
        return "error"


def GetDevice():
    lstNVR = GetAllNVR()
    lstCam = GetAllCamera()
    return (lstNVR, lstCam)

def GetAllNVR():
    conn = pymssql.connect(db_server, db_user, db_password,db_database)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(f'select * from {db_table_nvr}')
    lstDev = [{
                "Name": f"{row['NVSYM'].strip()}", 
                "IP": f"{row['NVIP'].strip()}",
                "Port": f"{row['NVPT']}",
                "Type": "NVR"
            } for row in cursor if row['NVIP'].strip()!= ""]
    conn.close()
    return lstDev

def GetAllCamera():
    conn = pymssql.connect(db_server, db_user, db_password,db_database)
    cursor = conn.cursor(as_dict=True)
    cursor.execute(f'select * from {db_table_dev}')
    #cursor.fetchall()
    #print(cursor.rowcount)
    lstNVR = [{
                "Name": f"{row['DEVSYM'].strip()} / {row['DEVNM'].strip()}", 
                "IP": f"{row['DEFIP'].strip()}",
                "Port": f"{row['DEFPT']}",
                "Type": "Camera"
            } for row in cursor if row['DEFIP'].strip()!= ""]
    # for row in lstDev:
    #     print(f"Camera : {row['DEVSYM'].strip()}/{row['DEVNM'].strip()} \t IP:{row['DEFIP,'].strip()}:{row['DEFPT']}")
    
    conn.close()
    return lstNVR

if __name__ == "__main__":
    print("starting main application")
    GetDBInfo()
    lstNVR, lstCam = GetDevice()
    print("Get list of NVR")
    print("----------------------------")
    print(lstNVR)
    print('')
    print("*****************************")
    print('')
    print("Get list of device")
    print("----------------------------")
    print(lstCam)



