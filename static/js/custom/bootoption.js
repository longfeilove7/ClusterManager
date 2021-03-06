/**
* 遍历表格内容返回数组
* @param Int  id 表格id
* @return Array
*/
function toBootDisk(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    var getPowerOn = $("#btn1_" + getID);
    //console.log(getPowerOn)
    var getPowerOff = $("#btn2_" + getID);
    //console.log(getPowerOff)
    var getPowerCycle = $("#btn3_" + getID);
    //console.log(getPowerCycle)

    $.confirm({
        title: '对如下设备进行硬盘启动?',
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
                        url: "/boot_disk/",
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
                                e.parentNode.parentNode.parentNode.children[13].innerHTML = data[1]
                                getPowerOn.attr('disabled', true);
                                getPowerOff.attr('disabled', false);
                                getPowerCycle.attr('disabled', false);
                                getPowerOn.children().css('color', 'grey');
                                getPowerOff.children().css('color', 'red');
                                getPowerCycle.children().css('color', 'yellowgreen');
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


function toBootPxe(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    var getPowerOn = $("#btn1_" + getID);
    //console.log(getPowerOn)
    var getPowerOff = $("#btn2_" + getID);
    //console.log(getPowerOff)
    var getPowerCycle = $("#btn3_" + getID);
    //console.log(getPowerCycle)

    $.confirm({
        title: '对如下设备进行PXE启动?',
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
                        url: "/boot_pxe/",
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
                                e.parentNode.parentNode.parentNode.children[13].innerHTML = data[1]
                                getPowerOn.attr('disabled', true);
                                getPowerOff.attr('disabled', false);
                                getPowerCycle.attr('disabled', false);
                                getPowerOn.children().css('color', 'grey');
                                getPowerOff.children().css('color', 'red');
                                getPowerCycle.children().css('color', 'yellowgreen');
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
function toBootCdrom(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    var getPowerOn = $("#btn1_" + getID);
    //console.log(getPowerOn)
    var getPowerOff = $("#btn2_" + getID);
    //console.log(getPowerOff)
    var getPowerCycle = $("#btn3_" + getID);
    //console.log(getPowerCycle)

    $.confirm({
        title: '对如下设备进行光驱启动?',
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
                        url: "/boot_cdrom/",
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
                                e.parentNode.parentNode.parentNode.children[14].innerHTML = data[1]
                                e.parentNode.parentNode.parentNode.children[16].innerHTML = '<a href="/power_history-' + getID + '/">' + data[3] + '</a>'
                                getPowerOn.attr('disabled', false);
                                getPowerOff.attr('disabled', true);
                                getPowerCycle.attr('disabled', true);
                                getPowerOn.children().css('color', 'green');
                                getPowerOff.children().css('color', 'grey');
                                getPowerCycle.children().css('color', 'grey');
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
function toBootBios(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var getIP = e.parentNode.parentNode.parentNode.children[8].innerHTML;
    $.confirm({
        title: '对如下设备进行BIOS启动?',
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
                        url: "/boot_bios/",
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
function toBatchBootDisk(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
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
        //    var getIP = e.parentNode.parentNode.children[8].innerHTML;
        console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        $.confirm({
            title: '对如下设备进行硬盘启动?',
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
                            url: "/batch_boot_disk/",
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
                                    var getPowerOn = $("#btn1_" + getID);
                                    //console.log(getPowerOn)
                                    var getPowerOff = $("#btn2_" + getID);
                                    //console.log(getPowerOff)
                                    var getPowerCycle = $("#btn3_" + getID);
                                    //console.log(getPowerCycle)
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
                                        mytable.rows[rowID].cells[13].innerHTML = newdata[2];
                                        getPowerOn.attr('disabled', true);
                                        getPowerOff.attr('disabled', false);
                                        getPowerCycle.attr('disabled', false);
                                        getPowerOn.children().css('color', 'grey');
                                        getPowerOff.children().css('color', 'red');
                                        getPowerCycle.children().css('color', 'yellowgreen');
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
function toBatchBootPxe(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
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
        //    var getIP = e.parentNode.parentNode.children[8].innerHTML;
        console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        $.confirm({
            title: '对如下设备进行PXE启动?',
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
                            url: "/batch_boot_pxe/",
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
                                    var getPowerOn = $("#btn1_" + getID);
                                    //console.log(getPowerOn)
                                    var getPowerOff = $("#btn2_" + getID);
                                    //console.log(getPowerOff)
                                    var getPowerCycle = $("#btn3_" + getID);
                                    //console.log(getPowerCycle)
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
                                        mytable.rows[rowID].cells[13].innerHTML = newdata[2];
                                        getPowerOn.attr('disabled', true);
                                        getPowerOff.attr('disabled', false);
                                        getPowerCycle.attr('disabled', false);
                                        getPowerOn.children().css('color', 'grey');
                                        getPowerOff.children().css('color', 'red');
                                        getPowerCycle.children().css('color', 'yellowgreen');
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
function toBatchBootCdrom(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
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
        //    var getIP = e.parentNode.parentNode.children[8].innerHTML;
        console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        $.confirm({
            title: '对如下设备进行光驱启动?',
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
                            url: "/batch_boot_cdrom/",
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
                                    var getPowerOn = $("#btn1_" + getID);
                                    //console.log(getPowerOn)
                                    var getPowerOff = $("#btn2_" + getID);
                                    //console.log(getPowerOff)
                                    var getPowerCycle = $("#btn3_" + getID);
                                    //console.log(getPowerCycle)
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
                                        mytable.rows[rowID].cells[14].innerHTML = newdata[2];
                                        mytable.rows[rowID].cells[16].innerHTML = '<a href="/power_history-' + getID + '/">' + newdata[4] + '</a>';
                                        getPowerOn.attr('disabled', false);
                                        getPowerOff.attr('disabled', true);
                                        getPowerCycle.attr('disabled', true);
                                        getPowerOn.children().css('color', 'green');
                                        getPowerOff.children().css('color', 'grey');
                                        getPowerCycle.children().css('color', 'grey');
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
function toBatchBootBios(id, e) {
    var allValue = queryCheckedValue()
    if (allValue.length == 0) {
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
        //    var getIP = e.parentNode.parentNode.children[8].innerHTML;
        console.log(allValue)
        strAllValue = allValue.join("-");
        console.log(strAllValue)
        $.confirm({
            title: '对如下设备进行BIOS启动?',
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
                            url: "/batch_boot_bios/",
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


