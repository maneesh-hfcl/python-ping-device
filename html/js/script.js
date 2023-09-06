const sse_url = "http://127.0.0.1:8088/sse-ping"
var evtSource;

$(document).ready(() => {
   // startPing()
})

const startPing = ()=>{
    evtSource = new EventSource(sse_url);
    evtSource.onmessage = (event)=>{
        let jsonData = JSON.parse(event.data)
        jsonData.status = jsonData.status == "Active"?"Connected":"Disconnected";
        console.log(`${jsonData.ip} / ${jsonData.status} / ${jsonData.dt} / ${jsonData.info}`)
        passData(jsonData)
    }
  //  alert("Going to start the ping")
}

const stopPing = ()=>{
    evtSource.close()
}

const passData = (jsonData)=>{
    let tbldata = $("#tblData")
    isSelected = false
    $.each($("#tblData > tbody > tr"), (indx, value)=>{
//        console.log($(value).find("td").eq(1).html() + " --- " + jsonData.ip)
        if($(value).find("td").eq(1).html() == jsonData.ip)
        {
            console.log("selected")
            $(value).find("td").eq(0).html(jsonData.dt)
            $(value).find("td").eq(2).html(jsonData.status)
            $(value).find("td").eq(3).html(jsonData.info)
            $(value).find("td").eq(2).removeClass()

            if(jsonData.status=="Connected")
                $(value).find("td").eq(2).addClass("active")
            else
                $(value).find("td").eq(2).addClass("inactive")

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
        htmlrow += `<td>${jsonData.ip}</td>`
        htmlrow += `<td class='${jsonData.status=="Connected"?"active":"inactive"}'>${jsonData.status}</td>`
        htmlrow += `<td>${jsonData.info}</td>`
        htmlrow += "</tr>"

        tbldata.append(htmlrow)
    }
}