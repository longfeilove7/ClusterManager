/**
* 遍历表格内容返回数组
* @param Int  id 表格id
* @return Array
*/
function toPowerOn(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    $.confirm({
        title: '对如下设备开机?',
        content: '设备IP：' + getIP,
        type: 'green',
        buttons: {
            ok: {
                text: "提交",
                btnClass: 'btn-primary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked confirm');
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
                            if (data[2] == "fail") {
                                $.alert({
                                    title: '提示：',
                                    content: "设备IP：" + data[0] + " 开机失败！",
                                    type: 'red',
                                    buttons: {
                                        ok: {
                                            text: "关闭",
                                            btnClass: 'btn-secondary',
                                            keys: ['enter']
                                        }
                                    }
                                })
                            }
                            else {                                
                                var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                //$table.bootstrapTable('destroy');
                                $table.bootstrapTable('refresh', opt);
                            }
                        },
                        error: function (request, info, e) {
                            alert("false");
                        }
                    })
                }
            },
            cancel: {
                text: "关闭",
                btnClass: 'btn-secondary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked cancel');
                }
            }
        }
    })
}




/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toPowerOff(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    $.confirm({
        title: '对如下设备关机?',
        content: '设备IP：' + getIP,
        type: 'green',
        buttons: {
            ok: {
                text: "提交",
                btnClass: 'btn-primary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked confirm');
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
                            if (data[2] == "fail") {
                                $.alert({
                                    title: '提示：',
                                    content: "设备IP：" + data[0] + " 关机失败！",
                                    type: 'red',
                                    buttons: {
                                        ok: {
                                            text: "关闭",
                                            btnClass: 'btn-secondary',
                                            keys: ['enter']
                                        }
                                    }
                                })
                            }
                            else {
                                var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                //$table.bootstrapTable('destroy');
                                $table.bootstrapTable('refresh', opt);
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
            },
            cancel: {
                text: "关闭",
                btnClass: 'btn-secondary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked cancel');
                }
            }
        }
    })
}





/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toPowerCycle(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    $.confirm({
        title: '对如下设备重启?',
        content: '设备IP：' + getIP,
        type: 'green',
        buttons: {
            ok: {
                text: "提交",
                btnClass: 'btn-primary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked confirm');
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
                            if (data[2] == "fail") {
                                $.alert({
                                    title: '提示：',
                                    content: "设备IP：" + data[0] + " 重启失败！",
                                    type: 'red',
                                    buttons: {
                                        ok: {
                                            text: "关闭",
                                            btnClass: 'btn-secondary',
                                            keys: ['enter']
                                        }
                                    }
                                })
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
            },
            cancel: {
                text: "关闭",
                btnClass: 'btn-secondary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked cancel');
                }
            }
        }
    })
}




/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toBatchPowerOn(id, e) {
    var rowObject = $("#mytable").bootstrapTable('getSelections');
    var row = JSON.stringify(rowObject);
    if (rowObject.length == 0) {
        $.alert({
            title: '提示：',
            content: '请先选择设备！',
            type: 'red',
            buttons: {
                ok: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter']
                }
            }
        })
    }
    else {
        $.confirm({
            title: '对如下设备开机?',
            content: '设备数量：' + rowObject.length,
            type: 'green',
            buttons: {
                ok: {
                    text: "提交",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked confirm');
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/batch_power_on/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': row
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
                                        if ($($(this).find("td").get(1)).text() == getID) {
                                            index = i - 1;
                                            //console.log("index" + index)
                                        }
                                    })
                                    rowID = index;
                                    console.log("rowID " + rowID)
                                    //e.parentNode.parentNode.children[13].innerHTML=data[1]

                                    if (newdata[3] == "fail") {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备IP：" + newdata[1] + " 开机失败！",
                                            type: 'red',
                                            buttons: {
                                                ok: {
                                                    text: "关闭",
                                                    btnClass: 'btn-secondary',
                                                    keys: ['enter']
                                                }
                                            }
                                        })
                                    }
                                    else {
                                        var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                        //$table.bootstrapTable('destroy');
                                        $table.bootstrapTable('refresh', opt);
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
                },
                cancel: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked cancel');
                    }
                }
            }
        })
    }
}





/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toBatchPowerOff(id, e) {
    var rowObject = $("#mytable").bootstrapTable('getSelections');
    var row = JSON.stringify(rowObject);
    if (rowObject.length == 0) {
        $.alert({
            title: '提示：',
            content: '请先选择设备！',
            type: 'red',
            buttons: {
                ok: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter']
                }
            }
        })
    }
    else {
        $.confirm({
            title: '对如下设备开机?',
            content: '设备数量：' + rowObject.length,
            type: 'green',
            buttons: {
                ok: {
                    text: "提交",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked confirm');
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/batch_power_off/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': row
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
                                        if ($($(this).find("td").get(1)).text() == getID) {
                                            index = i - 1;
                                            //console.log("index" + index)
                                        }
                                    })
                                    rowID = index;
                                    console.log("rowID " + rowID)
                                    //e.parentNode.parentNode.children[13].innerHTML=data[1]

                                    if (newdata[3] == "fail") {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备IP：" + newdata[1] + " 关机失败！",
                                            type: 'red',
                                            buttons: {
                                                ok: {
                                                    text: "关闭",
                                                    btnClass: 'btn-secondary',
                                                    keys: ['enter']
                                                }
                                            }
                                        })

                                    }
                                    else {
                                        var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                        //$table.bootstrapTable('destroy');
                                        $table.bootstrapTable('refresh', opt);
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
                },
                cancel: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked cancel');
                    }
                }
            }
        })
    }
}


/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toBatchPowerCycle(id, e) {
    var rowObject = $("#mytable").bootstrapTable('getSelections');
    var row = JSON.stringify(rowObject);
    if (rowObject.length == 0) {
        $.alert({
            title: '提示：',
            content: '请先选择设备！',
            type: 'red',
            buttons: {
                ok: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter']
                }
            }
        })
    }
    else {

        $.confirm({
            title: '对如下设备重启?',
            content: '设备数量：' + rowObject.length,
            type: 'green',
            buttons: {
                ok: {
                    text: "提交",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked confirm');
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/batch_power_cycle/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': row
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
                                        if ($($(this).find("td").get(1)).text() == getID) {
                                            index = i - 1;
                                            //console.log("index" + index)
                                        }
                                    })
                                    rowID = index;
                                    console.log("rowID " + rowID)
                                    //e.parentNode.parentNode.children[13].innerHTML=data[1]                                    
                                    if (newdata[2] == "fail") {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备IP：" + newdata[1] + " 重启失败！",
                                            type: 'red',
                                            buttons: {
                                                ok: {
                                                    text: "关闭",
                                                    btnClass: 'btn-secondary',
                                                    keys: ['enter']
                                                }
                                            }
                                        })
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
                },
                cancel: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked cancel');
                    }
                }
            }
        })
    }
}


/**
* 遍历表格内容返回数组
* @param Int  id 表格id
* @return Array
*/
function toBatchInspectSdr(id, e) {
    var rowObject = $("#mytable").bootstrapTable('getSelections');
    var row = JSON.stringify(rowObject);
    if (rowObject.length == 0) {
        $.alert({
            title: '提示：',
            content: '请先选择设备！',
            type: 'red',
            buttons: {
                ok: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter']
                }
            }
        })
    }
    else {
        $.confirm({
            title: '对如下设备巡检?',
            content: '设备数量：' + allValue.length,
            type: 'green',
            buttons: {
                ok: {
                    text: "提交",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked confirm');
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/batch_inspect_sdr/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': row
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
                                        //list the row id ,index .get(1)
                                        if ($($(this).find("td").get(1)).text() == getID) {
                                            index = i - 1;
                                            //console.log("index" + index)
                                        }
                                    })
                                    rowID = index;
                                    console.log("rowID " + rowID)
                                    //e.parentNode.parentNode.children[13].innerHTML=data[1]
                                    mytable.rows[rowID].cells[14].innerHTML = newdata[2];
                                    mytable.rows[rowID].cells[16].innerHTML = newdata[4];
                                    if (newdata[3] == "fail") {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备IP：" + newdata[1] + " 巡检失败！",
                                            type: 'red',
                                            buttons: {
                                                ok: {
                                                    text: "关闭",
                                                    btnClass: 'btn-secondary',
                                                    keys: ['enter']
                                                }
                                            }
                                        })
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
                },
                cancel: {
                    text: "关闭",
                    btnClass: 'btn-secondary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked cancel');
                    }
                }
            }
        })
    }
}

/**
 * 遍历表格内容返回数组
 * @param Int  id 表格id
 * @return Array
 */
function toInspectSdr(id, e) {
    var getID = e.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.children[8].innerHTML;

    $.confirm({
        title: '对如下设备巡检?',
        content: '设备IP：' + getIP,
        type: 'green',
        buttons: {
            ok: {
                text: "提交",
                btnClass: 'btn-primary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked confirm');
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
                            e.parentNode.parentNode.children[14].innerHTML = data[1]
                            e.parentNode.parentNode.children[16].innerHTML = data[3]
                            if (data[2] == "fail") {

                                $.alert({
                                    title: '提示：',
                                    content: "设备IP：" + data[0] + " 关机失败！",
                                    type: 'red',
                                    buttons: {
                                        ok: {
                                            text: "关闭",
                                            btnClass: 'btn-secondary',
                                            keys: ['enter']
                                        }
                                    }
                                })
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
            },
            cancel: {
                text: "关闭",
                btnClass: 'btn-secondary',
                keys: ['enter'],
                action: function () {
                    console.log('the user clicked cancel');
                }
            }
        }
    })
}