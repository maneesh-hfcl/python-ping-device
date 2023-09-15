//const sse_url = "http://127.0.0.1:8088/sse-ping"
const sse_url = "/sse-ping-db-device"
const sse_url_dev_port = "/sse-ping-device"

var evtSource;

$(document).ready(() => {
   // startPing()
})

const pingDevice = (btn)=>{
    if(btn.html() == "Start")
    {
        btn.html("Stop")
        btn.removeClass("btn-success")
        btn.addClass("btn-danger")
        $("#divLoading").show()
        startPing(sse_url)

    }
    else
    {
        btn.html("Start")
        btn.removeClass("btn-danger")
        btn.addClass("btn-success")
        stopPingDevice()
    }

}
const pingDevicePort = ()=> startPing(sse_url_dev_port)

const startPing = (url)=>{
    evtSource = new EventSource(url);
    evtSource.onmessage = (event)=>{
        $("#divLoading").hide()
        let jsonData = JSON.parse(event.data)
        jsonData.status = jsonData.status == "Active"?"Connected":"Disconnected";
        console.log(`${jsonData.ip} / ${jsonData.status} / ${jsonData.dt} / ${jsonData.info}`)
        passData(jsonData)
    }
  //  alert("Going to start the ping")
}

const stopPing = async()=>{
    evtSource.close()
    let evnt_stop_url = "/stoppingdev"
    let myobject = await fetch(evnt_stop_url)
    let mytext = await myobject.text()
    console.log(mytext)
}

const stopPingDevice = ()=> stopPing()


const passData = (jsonData)=>{
    let tbldata = $("#tblData")
    isSelected = false
    $.each($("#tblData > tbody > tr"), (indx, value)=>{
//        console.log($(value).find("td").eq(1).html() + " --- " + jsonData.ip)
        if($(value).find("td").eq(3).html() == jsonData.ip)
        {
            console.log("selected")
            $(value).find("td").eq(0).html(jsonData.dt)
            //$(value).find("td").eq(1).html(jsonData.type)
            //$(value).find("td").eq(2).html(jsonData.name)
            $(value).find("td").eq(4).html(jsonData.status)
        //    $(value).find("td").eq(5).html(jsonData.info)
            $(value).find("td").eq(4).removeClass()

            if(jsonData.status=="Connected")
                $(value).find("td").eq(4).addClass("active")
            else
                $(value).find("td").eq(4).addClass("inactive")

            //console.log("select ip: " + jsonData.ip)
            isSelected = true
            return false;
        }
   //     console.log(`Index: ${indx}; value: ${value.cells[0].innerHTML}`)
    });
    if(!isSelected)
    {
        console.log("Adding row:" + jsonData)
        let htmlrow = "<tr>"
        htmlrow += `<td>${jsonData.dt}</td>`
        htmlrow += `<td>${jsonData.type}</td>`
        htmlrow += `<td>${jsonData.name}</td>`
        htmlrow += `<td>${jsonData.ip}</td>`
        htmlrow += `<td class='${jsonData.status=="Connected"?"active":"inactive"}'>${jsonData.status}</td>`
       // htmlrow += `<td>${jsonData.info}</td>`
        htmlrow += "</tr>"

        tbldata.append(htmlrow)
    }
}