//页面监听函数
$(function () /*to init open the html*/ {
    //判断访问链接，设置打开的tab标签
    var url = location.href
    //alert(url)
    //判断路径是否含有#
    if (url.search("#") != -1) {
        var tabIl = url.split("#")[1].split("menu")[1];
        //alert(tabIl)    
        $("#myTab li:eq(" + tabIl + ") a").tab("show");
    }
    //判断按钮值，设置按钮属性
    var getPowerOn = $("#powerOn");
    //console.log(getPowerOn)
    var getPowerOff = $("#powerOff");
    //console.log(getPowerOff)
    var getPowerCycle = $("#powerCycle");
    //console.log(getPowerCycle)
    var getPowerStatus = $("#powerStatus");
    var getValue = getPowerOn.val();//.attr("value")和.val()都可以
    //alert(getValue)
    //0:poweroff 1:poweron 2:powercycle
    if (getValue == 0) {
        getPowerOn.attr('disabled', false);
        getPowerOff.attr('disabled', true);
        getPowerCycle.attr('disabled', true);
        getPowerOn.children().css('color', 'green');
        getPowerOff.children().css('color', 'grey');
        getPowerCycle.children().css('color', 'grey');
        getPowerStatus.children().css('color', 'grey');
    }
    else if (getValue == 1) {
        getPowerOn.attr('disabled', true);
        getPowerOff.attr('disabled', false)
        getPowerCycle.attr('disabled', false);
        getPowerOn.children().css('color', 'grey');
        getPowerOff.children().css('color', 'red');
        getPowerCycle.children().css('color', 'yellowgreen');
        getPowerStatus.children().css('color', 'yellowgreen');
    }
    else {
        getPowerOn.attr('disabled', true);
        getPowerOff.attr('disabled', true);
        getPowerCycle.attr('disabled', true);
        getPowerOn.css('color', 'grey');
        getPowerOff.css('color', 'grey');
        getPowerCycle.css('color', 'grey');
        getPowerStatus.children().css('color', 'red');
    };
});
/**
* 遍历表格内容返回数组
* @param Int  id 表格id
* @return Array
*/

function toPowerOn(id, e) {
    var getID = $('#getID').text();
    var getIP = $('#ipmi').val();
    var getPowerOn = $("#powerOn");
    //console.log(getPowerOn)
    var getPowerOff = $("#powerOff");
    //console.log(getPowerOff)
    var getPowerCycle = $("#powerCycle");
    //console.log(getPowerCycle)
    var getPowerStatus = $("#powerStatus");
    var getValue = getPowerOn.val();//.attr("value")和.val()都可以
    //alert(getValue)
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
                                getPowerOn.attr('disabled', true);
                                getPowerOff.attr('disabled', false);
                                getPowerCycle.attr('disabled', false);
                                getPowerOn.children().css('color', 'grey');
                                getPowerOff.children().css('color', 'red');
                                getPowerCycle.children().css('color', 'yellowgreen');
                                getPowerStatus.children().css('color', 'yellowgreen');
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
    var getID = $('#getID').text();
    var getIP = $('#ipmi').val();
    var getPowerOn = $("#powerOn");
    //console.log(getPowerOn)
    var getPowerOff = $("#powerOff");
    //console.log(getPowerOff)
    var getPowerCycle = $("#powerCycle");
    //console.log(getPowerCycle)
    var getPowerStatus = $("#powerStatus");
    var getValue = getPowerOn.val();//.attr("value")和.val()都可以
    //alert(getValue)
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
                                getPowerOn.attr('disabled', false);
                                getPowerOff.attr('disabled', true);
                                getPowerCycle.attr('disabled', true);
                                getPowerOn.children().css('color', 'green');
                                getPowerOff.children().css('color', 'grey');
                                getPowerCycle.children().css('color', 'grey');
                                getPowerStatus.children().css('color', 'grey');
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
    var getID = $('#getID').text();
    var getIP = $('#ipmi').val();
    var getPowerOn = $("#powerOn");
    //console.log(getPowerOn)
    var getPowerOff = $("#powerOff");
    //console.log(getPowerOff)
    var getPowerCycle = $("#powerCycle");
    //console.log(getPowerCycle)
    var getPowerStatus = $("#powerStatus");
    var getValue = getPowerOn.val();//.attr("value")和.val()都可以
    //alert(getValue)
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




