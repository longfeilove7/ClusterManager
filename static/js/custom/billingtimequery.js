function getFormatDate() {
    var nowDate = new Date();
    var year = nowDate.getFullYear();
    var month = nowDate.getMonth() + 1 < 10 ? "0" + (nowDate.getMonth() + 1) : nowDate.getMonth() + 1;
    var date = nowDate.getDate() < 10 ? "0" + nowDate.getDate() : nowDate.getDate();
    var hour = nowDate.getHours() < 10 ? "0" + nowDate.getHours() : nowDate.getHours();
    var minute = nowDate.getMinutes() < 10 ? "0" + nowDate.getMinutes() : nowDate.getMinutes();
    var second = nowDate.getSeconds() < 10 ? "0" + nowDate.getSeconds() : nowDate.getSeconds();
    return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
}
function getFormatDateZero() {
    var todayZero = new Date();
    var year = todayZero.getFullYear();
    var month = todayZero.getMonth() + 1 < 10 ? "0" + (todayZero.getMonth() + 1) : todayZero.getMonth() + 1;
    var date = todayZero.getDate() < 10 ? "0" + todayZero.getDate() : todayZero.getDate();
    return year + "-" + month + "-" + date + " " + "00" + ":" + "00" + ":" + "00";
}
function postDateTime() {
    // 初始化内容   
    var startDateTime = getFormatDateZero();
    var endDateTime = getFormatDate();
    console.log("the startDateTime:" + startDateTime)
    console.log("the endDateTime:" + endDateTime)
    $.ajax({
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        //contentType: "application/json; charset=utf-8", //django not support json,don't use this
        dataType: "json", //for to get json
        url: "/billing_time_query/",
        type: "POST",
        cache: false,
        data: {
            'startDateTime': startDateTime,
            'endDateTime': endDateTime,
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
        }
    })
}
//页面初始化函数，初始化时提交当前时间
$(document).ready(function () {
    postDateTime();
});

//表格监听刷新按钮函数
var $table = $('#mytable');
$table.on('refresh.bs.table', function () {
    postDateTime();
}
)
$table.on('load-success.bs.table column-switch.bs.table page-change.bs.table search.bs.table', function () {

})
//自定义时间监控查询函数
function toBillingTimeQuery(id, e) {
    var startDateTime = $("#startDateTime").val();//.attr("value")和.val()都可以
    console.log(startDateTime);
    var endDateTime = $("#endDateTime").val();//.attr("value")和.val()都可以
    console.log(endDateTime)
    if (startDateTime == "") {
        $.alert({
            title: '提示：',
            content: '请选择开始时间！',
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
    else if (endDateTime == "") {
        $.alert({
            title: '提示：',
            content: '请选择结束时间！',
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
    else if (endDateTime <= startDateTime) {
        $.alert({
            title: '提示：',
            content: '结束时间必须大于开始时间！',
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
            title: '根据如下时间开始查询?',
            content: '开始时间：' + startDateTime + ' \n ' + '结束时间：' + endDateTime,
            type: 'green',
            buttons: {
                ok: {
                    text: "提交",
                    btnClass: 'btn-primary',
                    keys: ['enter'],
                    action: function () {
                        console.log('the user clicked confirm');
                        var startDateTime = $("#startDateTime").val();//.attr("value")和.val()都可以
                        console.log(startDateTime);
                        var endDateTime = $("#endDateTime").val();//.attr("value")和.val()都可以
                        console.log(endDateTime)
                        $.ajax({
                            contentType: "application/x-www-form-urlencoded; charset=utf-8",
                            //contentType: "application/json; charset=utf-8", //django not support json,don't use this
                            dataType: "json", //for to get json
                            url: "/billing_time_query/",
                            type: "POST",
                            cache: false,
                            data: {
                                'startDateTime': startDateTime,
                                'endDateTime': endDateTime,
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
                                var opt = { url: "/billing_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                //$table.bootstrapTable('destroy');
                                $table.bootstrapTable('refresh', opt);
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
