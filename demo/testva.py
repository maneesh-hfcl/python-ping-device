import requests

def fn_testVAEvents():
    print("testing va events")
    url = "http://172.17.35.185:8822/api/datarec"
    event_data = {
        "cameraIP":"cam1",
        "evtType":"Tripwire",
        "dtEvnt":"2023-09-09",
        "imgArray":""
    }

    res = requests.post(url=url, json=event_data)
    print(res.text)

if __name__ == "__main__":
    fn_testVAEvents()