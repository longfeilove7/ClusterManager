    // using jQuery
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
    // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    break;
}
}
}
return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
        beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
}
});

/**
* 遍历表格内容返回数组
* @param Int  id 表格id
* @return Array
*/
function toPowerOn(id, e) {
    var getID = e.parentNode.parentNode.children[0].innerHTML;
    var getIP = e.parentNode.parentNode.children[7].innerHTML;

    if (confirm("Power on " + getIP)) {
        $.ajax({
            contentType: "application/x-www-form-urlencoded; charset=utf-8",
            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
            dataType: "json", //for to get json
            url: "/power_on/",
            type: "POST",
            cache: false,
            data: {
                'ID': getID,
                'IP': getIP
            },
            beforeSend: function (xhr, settings) {
                //此处调用刚刚加入的js方法
                var csrftoken = getCookie('csrftoken');
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data) {
                console.log(data)
                //alert(data)
                //以上是后端函数返回成功的信息
                e.parentNode.parentNode.children[15].innerHTML = data[1]
                if (data[2] == "fail") {
                    alert(data[0] + "poweron" + data[2])
                }
            },
            error: function (request, info, e) {
                alert("false");                
            }
        })
    }
    }
    

 

/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toPowerOff(id, e) {
    var getID = e.parentNode.parentNode.children[0].innerHTML;
        var getIP = e.parentNode.parentNode.children[7].innerHTML;
    
    if (confirm("Power off " + getIP)) {
            $.ajax({
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                dataType: "json", //for to get json
                url: "/power_off/",
                type: "POST",
                cache: false,
                data: {
                    'ID': getID,
                    'IP': getIP
                },
                beforeSend: function (xhr, settings) {
                    //此处调用刚刚加入的js方法
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    e.parentNode.parentNode.children[16].innerHTML = data[1]
                    e.parentNode.parentNode.children[18].innerHTML = data[3]
                    if (data[2] == "fail") {
                        alert(data[0] + "poweroff" + data[2])
                    }
                    console.log(data)
                    //alert(data[1])
                    //以上是后端函数返回成功的信息
                },
                error: function (request, info, e) {
                    alert("false");
                    console.log(e)
                }
            })
        }
        }
        




/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toPowerCycle(id, e) {
    var getID = e.parentNode.parentNode.children[0].innerHTML;
        var getIP = e.parentNode.parentNode.children[7].innerHTML;
    
    if (confirm("Power cycle " + getIP)) {
            $.ajax({
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                dataType: "json", //for to get json
                url: "/power_cycle/",
                type: "POST",
                cache: false,
                data: {
                    'ID': getID,
                    'IP': getIP
                },
                beforeSend: function (xhr, settings) {
                    //此处调用刚刚加入的js方法
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    e.parentNode.parentNode.children[15].innerHTML = data[1]
                    if (data[2] == "fail") {
                        alert(data[0] + "poweron" + data[2])
                    }
                    console.log(data)
                    //alert(data[1])
                    //以上是后端函数返回成功的信息
                },
                error: function (request, info, e) {
                    alert("false");
                    console.log(e)
                }
            })
        }
        }
        

 

/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toBatchPowerOn(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
            alert("null")
        }
        else {
            //    var getIP = e.parentNode.parentNode.children[7].innerHTML;
            console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        if (confirm("batch Power On [ " + allValue.length + " ] server")) {
            $.ajax({
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                dataType: "json", //for to get json
                url: "/batch_power_on/",
                type: "POST",
                cache: false,
                data: {
                    'allValue': strAllValue
                },
                beforeSend: function (xhr, settings) {
                    //此处调用刚刚加入的js方法
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    console.log(data)
                    for (var i = 0; i < data.length; i++) {
                        //console.log("shis" + data[i]);
                        var newdata = new Array();
                        newdata = data[i];
                        console.log(newdata);
                        getID = newdata[0];
                        var index = 0;
                        // from the ID to get the rowID
                        $("table tr").each(function (i) {

                            if ($($(this).find("td").get(0)).text() == getID) {
                                index = i;
                                //console.log("index" + index)
                            }
                        })
                        rowID = index;
                        console.log("rowID " + rowID)
                        //e.parentNode.parentNode.children[15].innerHTML=data[1]
                        mytable.rows[rowID].cells[15].innerHTML = newdata[2];
                        if (newdata[3] == "fail") {
                            alert(newdata[1] + "poweron" + newdata[3]);
                        }
                    }
                    //alert(data[1])
                    //以上是后端函数返回成功的信息
                },
                error: function (request, info, e) {
                    alert("false");
                    console.log(e)
                }
            })
        }
        }
    }
    




/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toBatchPowerOff(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
            alert("null")
        }
        else {
            //    var getIP = e.parentNode.parentNode.children[7].innerHTML;
            console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        if (confirm("batch Power Off [ " + allValue.length + " ] server")) {
            $.ajax({
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                dataType: "json", //for to get json
                url: "/batch_power_off/",
                type: "POST",
                cache: false,
                data: {
                    'allValue': strAllValue
                },
                beforeSend: function (xhr, settings) {
                    //此处调用刚刚加入的js方法
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    console.log(data)
                    for (var i = 0; i < data.length; i++) {
                        //console.log("shis" + data[i]);
                        var newdata = new Array();
                        newdata = data[i];
                        console.log(newdata);
                        getID = newdata[0];
                        var index = 0;
                        // from the ID to get the rowID
                        $("table tr").each(function (i) {

                            if ($($(this).find("td").get(0)).text() == getID) {
                                index = i;
                                //console.log("index" + index)
                            }
                        })
                        rowID = index;
                        console.log("rowID " + rowID)
                        //e.parentNode.parentNode.children[15].innerHTML=data[1]
                        mytable.rows[rowID].cells[16].innerHTML = newdata[2];
                        mytable.rows[rowID].cells[18].innerHTML = newdata[4];
                        if (newdata[3] == "fail") {
                            alert(newdata[1] + "poweroff" + newdata[3]);
                        }
                    }
                    //alert(data[1])
                    //以上是后端函数返回成功的信息
                },
                error: function (request, info, e) {
                    alert("false");
                    console.log(e)
                }
            })
        }
        }
    }



    /**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toBatchInspectSdr(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
            alert("null")
        }
        else {
            //    var getIP = e.parentNode.parentNode.children[7].innerHTML;
            console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        if (confirm("batch Inspect sdr [ " + allValue.length + " ] server")) {
            $.ajax({
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                dataType: "json", //for to get json
                url: "/batch_inspect_sdr/",
                type: "POST",
                cache: false,
                data: {
                    'allValue': strAllValue
                },
                beforeSend: function (xhr, settings) {
                    //此处调用刚刚加入的js方法
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    console.log(data)
                    for (var i = 0; i < data.length; i++) {
                        //console.log("shis" + data[i]);
                        var newdata = new Array();
                        newdata = data[i];
                        console.log(newdata);
                        getID = newdata[0];
                        var index = 0;
                        // from the ID to get the rowID
                        $("table tr").each(function (i) {

                            if ($($(this).find("td").get(0)).text() == getID) {
                                index = i;
                                //console.log("index" + index)
                            }
                        })
                        rowID = index;
                        console.log("rowID " + rowID)
                        //e.parentNode.parentNode.children[15].innerHTML=data[1]
                        mytable.rows[rowID].cells[16].innerHTML = newdata[2];
                        mytable.rows[rowID].cells[18].innerHTML = newdata[4];
                        if (newdata[3] == "fail") {
                            alert(newdata[1] + "inspectsdr" + newdata[3]);
                        }
                    }
                    //alert(data[1])
                    //以上是后端函数返回成功的信息
                },
                error: function (request, info, e) {
                    alert("false");
                    console.log(e)
                }
            })
        }
        }
    }

/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toInspectSdr(id, e) {
    var getID = e.parentNode.parentNode.children[0].innerHTML;
        var getIP = e.parentNode.parentNode.children[7].innerHTML;
    
    if (confirm("inspect sdr " + getIP)) {
            $.ajax({
                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                dataType: "json", //for to get json
                url: "/inspect_sdr/",
                type: "POST",
                cache: false,
                data: {
                    'ID': getID,
                    'IP': getIP
                },
                beforeSend: function (xhr, settings) {
                    //此处调用刚刚加入的js方法
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function (data) {
                    e.parentNode.parentNode.children[16].innerHTML = data[1]
                    e.parentNode.parentNode.children[18].innerHTML = data[3]
                    if (data[2] == "fail") {
                        alert(data[0] + "poweroff" + data[2])
                    }
                    console.log(data)
                    //alert(data[1])
                    //以上是后端函数返回成功的信息
                },
                error: function (request, info, e) {
                    alert("false");
                    console.log(e)
                }
            })
        }
        }