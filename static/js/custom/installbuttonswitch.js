//单个设备切换函数
function toButtonYesNo(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    var isChecked = $("#" + getID).is(":checked");
    //console.log(isChecked);
    if (isChecked) {
        tips = "取消";
        setValue = 0;
        $.confirm({
            title: '对如下设备' + tips + '待装列表?',
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
                            url: "/install_switch/",
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
        tips = "加入";
        setValue = 1;
        $.confirm({
            title: '对如下设备' + tips + '待装列表?',
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
                            url: "/install_switch/",
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
//多个设备设置加入待装列表系统函数
function toBatchButtonAdd(id, e) {
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
        //    var getIP = e.parentNode.parentNode.children[8].innerHTML;
        console.log(typeof row)
        console.log(row)
        $.confirm({
            title: '对如下设备加入待装列表?',
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
                            url: "/batch_install_add/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': row,
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
//多个设备取消待装列表系统函数
function toBatchButtonDelete(id, e) {
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
        //    var getIP = e.parentNode.parentNode.children[8].innerHTML;
        console.log(row)
        $.confirm({
            title: '对如下设备取消待装列表?',
            content: '设备数量：' + rowObject.length,
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
                            url: "/batch_install_delete/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': row,
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
