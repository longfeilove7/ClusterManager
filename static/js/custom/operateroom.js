/*         编辑房间的模态*/
function toEditRoom(id, e) {
    /*            获取当前点击事件标签上的id*/
    var getID = e.parentNode.parentNode.children[1].innerHTML;
    var getRoomName = e.parentNode.parentNode.children[2].innerHTML;
    var getCabinetNumber = e.parentNode.parentNode.children[3].innerHTML;
    var getFloor = e.parentNode.parentNode.children[4].innerHTML;
    var getRoomArea = e.parentNode.parentNode.children[5].innerHTML;  
    console.log("getid = " + getID)
    // document.body.onclick = function (event) { 部分浏览器不支持此方法，改用如上parentNode方式。
    //     var id = event.target.id;
    //     console.log(id);
    if (getID) {
        var link = "/room_edit-" + getID + '/';
        console.log(link);
        /*set the form action*/
        $('#editFormRoom').attr('action', link)
        $("#spanId").html(getID);
        //name selector $("input[name= ' '").val()            
        $("input[name='roomName']").val(getRoomName);
        $("input[name='cabinetNumber']").val(getCabinetNumber);
        $("input[name='floor']").val(getFloor);
        $("input[name='roomArea']").val(getRoomArea);     
    }
};

/*         删除的模态*/
function toDeleteRoom(id, e) {
    /*            获取当前点击事件标签上的id*/

    var getID = e.parentNode.parentNode.children[1].innerHTML;
    console.log("getid = " + getID)
    // document.body.onclick = function (event) { 部分浏览器不支持此方法，改用如上parentNode方式。
    //     var id = event.target.id;
    //     console.log(id);
    if (getID) {
        $.confirm({
            title: '删除如下房间?',
            content: '房间ID：' + getID,
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
                            url: "/room_delete/",
                            type: "POST",
                            cache: false,
                            data: {
                                'allValue': getID
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
                                getID = data[0];
                                console.log("the getID:" + getID);
                                getValue = data[1];
                                console.log("the getValue:" + getValue);
                                if (getValue == 1) {
                                    var opt = { url: "/room_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                    $table.bootstrapTable('refresh', opt);
                                }
                                else {
                                    $.alert({
                                        title: '提示：',
                                        content: "房间ID：" + data[0] + " 正在使用，删除失败！",
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
};


//多个房间删除函数

function toBatchDeleteRoom(id, e) {
    var rowObject = $("#mytable").bootstrapTable('getSelections');
    var row = JSON.stringify(rowObject);
    if (rowObject.length == 0) {
        $.alert({
            title: '提示：',
            content: '请先选择房间！',
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
            title: '删除如下房间?',
            content: '房间数量：' + rowObject.length,
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
                            url: "/batch_room_delete/",
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
                                    var newdata = new Array();
                                    newdata = data[i];
                                    console.log(newdata);
                                    getID = newdata[0];
                                    console.log("the getID:" + getID);
                                    getValue = newdata[1];
                                    console.log("the getValue:" + getValue);
                                    if (getValue == 1) {
                                        var opt = { url: "/room_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                        $table.bootstrapTable('refresh', opt);
                                    }
                                    else {
                                        $.alert({
                                            title: '提示：',
                                            content: "房间ID：" + newdata[0] + " 正在使用，删除失败！",
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
