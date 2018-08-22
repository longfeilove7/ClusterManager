function toButtonYes(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    //alert(getID);
    //采用jquery-confirm插件
    $.confirm({
        title: '对如下设备计费?',
        content: '设备ID：' + getID,
        type: 'green',
        buttons: {
            ok: {
                text: "是",
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
                            'ID': getID
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
                            //e.parentNode.parentNode.children[13].innerHTML = data[1]
                            // if (data[2] == "fail") {
                            //     alert(data[0] + "poweron" + data[2])
                            // }
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
                }
            }
        }
    });
}

function toButtonNo(id, e) {
    var getID = e.parentNode.parentNode.parentNode.children[1].innerHTML;
    $.confirm({
        title: '取消如下设备计费?',
        content: '设备ID：' + getID,
        type: 'green',
        buttons: {
            ok: {
                text: "是",
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
                            'ID': getID
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
                            //e.parentNode.parentNode.children[13].innerHTML = data[1]
                            // if (data[2] == "fail") {
                            //     alert(data[0] + "poweron" + data[2])
                            // }
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
                }
            }
        }
    });
    //alert(getID);
    //$('.buttonYes').removeClass('active');
    //$('.buttonNo').addClass('active');            
}