// //页面初始化函数，改用bootstrap-table自带表格监听函数
// $(document).ready(function () {
//     // 初始化内容
//     $("table tr").each(function () {    // 遍历每一行
//         var getBilling = $(this).children('td:eq(13)').children().children();  // td:eq(0)选择器表示第一个单元格
//         //console.log(getBilling);
//         var getValue = getBilling.val();//.attr("value")和.val()都可以
//         //console.log(getValue);
//         if (getValue == 1) {
//             getBilling.attr('checked', true);
//         }
//     });
// });

//表格监听函数

var $table = $('#mytable');
$table.on('load-success.bs.table column-switch.bs.table page-change.bs.table search.bs.table', function () {
    $("table tr").each(function () {    // 遍历每一行

        var getBilling = $(this).children('td:eq(13)').children().children();  // td:eq(0)选择器表示第一个单元格
        //console.log(getBilling);        
        var getValue = getBilling.val();//.attr("value")和.val()都可以
        //console.log(getValue);

        if (getValue == 1) {
            getBilling.attr('checked', true);
            getValue = 0
            //alert(getValue)
            getBilling.val(0);
        }
        else {
            getBilling.attr('checked', false);
        }
    });
});
//切换页码函数
// your custom ajax request here
function ajaxRequest(params) {
    // data you need
    //console.log(params.data);
    // just use setTimeout
    //$table.bootstrapTable('destroy').bootstrapTable();
    //$table.oTableInit();
    //$table.bootstrapTable('refresh');
    setTimeout(function () {
        //console.log("params.data");
        params.success({
            total: 100,
            rows: [{
                "id": 0,
                "name": "Item 0",
                "price": "$0"
            }]
        });
    }, 1000);
}
//单个设备切换函数
function toButtonYesNo(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var isChecked = $("#" + getID).is(":checked");
    //console.log(isChecked);
    if (isChecked) {
        tips = "暂停";
        setValue = 0;
        $.confirm({
            title: '对如下设备' + tips + '监控?',
            content: '设备ID：' + getID,
            type: 'red',
            buttons: {
                ok: {
                    text: "是",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        //console.log('the user clicked confirm');
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/monitor_switch/",
                            type: "POST",
                            cache: false,
                            data: {
                                'ID': getID,
                                'setValue': setValue,
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
                                //以上是后端函数返回成功的信息
                                var $getBilling = $("#" + getID);
                                $getBilling.attr('checked', false);
                                $getBilling.val(0);
                                console.log($getBilling.val());
                            },
                            error: function (request, info, e) {
                                alert("false");
                            }
                        })
                    }
                },
                cancel: {
                    text: "否",
                    btnClass: 'btn-secondary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked cancel');
                        $("#" + getID).attr('checked', true);
                    }
                }
            }
        });
    }
    else {
        tips = "开始";
        setValue = 1;
        $.confirm({
            title: '对如下设备' + tips + '监控?',
            content: '设备ID：' + getID,
            type: 'green',
            buttons: {
                ok: {
                    text: "是",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        //console.log('the user clicked confirm');
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/monitor_switch/",
                            type: "POST",
                            cache: false,
                            data: {
                                'ID': getID,
                                'setValue': setValue,
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
                                var $getBilling = $("#" + getID);
                                $getBilling.attr('checked', true);
                                $getBilling.val(1);
                                var $table = $('#mytable');
                            },
                            error: function (request, info, e) {
                                alert("false");
                            }
                        })
                    }
                },
                cancel: {
                    text: "否",
                    btnClass: 'btn-secondary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked cancel');
                        $("#" + getID).attr('checked', false);
                    }
                }
            }
        });
    }
}
//多个设备设置监控函数
function toBatchButtonAdd(id, e) {
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
            title: '对如下设备开始监控?',
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
                            url: "/batch_monitor_add/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': strAllValue,
                                'setValue': 1,
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
                                    var newdata = new Array();
                                    newdata = data[i];
                                    console.log(newdata);
                                    getID = newdata[0];
                                    console.log("the getID:" + getID);
                                    getValue = newdata[1];
                                    console.log("the getValue:" + getValue);
                                    if (getValue == 1) {
                                        $("#" + getID).attr('checked', true);
                                    }
                                    else {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备ID：" + newdata[0] + " 设置失败！",
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
//多个设备暂停监控函数
function toBatchButtonPause(id, e) {
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
            title: '对如下设备暂停监控?',
            content: '设备数量：' + allValue.length,
            type: 'red',
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
                            url: "/batch_monitor_delete/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': strAllValue,
                                'setValue': 0,
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
                                    var newdata = new Array();
                                    newdata = data[i];
                                    console.log(newdata);
                                    getID = newdata[0];
                                    console.log("the getID:" + getID);
                                    getValue = newdata[1];
                                    console.log("the getValue:" + getValue);
                                    if (getValue == 0) {
                                        $("#" + getID).attr('checked', false);
                                    }
                                    else {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备ID：" + newdata[0] + " 设置失败！",
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
//多个设备删除监控函数
function toBatchButtonDelete(id, e) {
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
            title: '对如下设备删除监控?',
            content: '设备数量：' + allValue.length,
            type: 'red',
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
                            url: "/batch_monitor_delete/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': strAllValue,
                                'setValue': 0,
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
                                    var newdata = new Array();
                                    newdata = data[i];
                                    console.log(newdata);
                                    getID = newdata[0];
                                    console.log("the getID:" + getID);
                                    getValue = newdata[1];
                                    console.log("the getValue:" + getValue);
                                    if (getValue == 0) {
                                        $("#" + getID).attr('checked', false);
                                    }
                                    else {
                                        $.alert({
                                            title: '提示：',
                                            content: "设备ID：" + newdata[0] + " 设置失败！",
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