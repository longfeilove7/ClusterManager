/*         编辑主机的模态*/
function toEditHost(id, e) {
    /*            获取当前点击事件标签上的id*/
    var getID = e.parentNode.parentNode.children[1].innerHTML;
    var getRoomNO = e.parentNode.parentNode.children[2].innerHTML;
    var getCabinetNO = e.parentNode.parentNode.children[3].innerHTML;
    var getBladeBoxNO = e.parentNode.parentNode.children[4].innerHTML;
    var getBladeNO = e.parentNode.parentNode.children[5].innerHTML;
    var getHostName = e.parentNode.parentNode.children[6].innerHTML;
    var getServiceIP = e.parentNode.parentNode.children[7].innerHTML;
    var getManageIP = e.parentNode.parentNode.children[8].innerHTML;
    var getStorageIP = e.parentNode.parentNode.children[9].innerHTML;
    var getClusterName = e.parentNode.parentNode.children[10].innerHTML;
    var getHardware = e.parentNode.parentNode.children[11].innerHTML;
    var getService = e.parentNode.parentNode.children[12].innerHTML;
    console.log("getid = " + getID)
    console.log("getClusterName" + getClusterName)
    // document.body.onclick = function (event) { 部分浏览器不支持此方法，改用如上parentNode方式。
    //     var id = event.target.id;
    //     console.log(id);
    if (getID) {
        var link = "/host_edit-" + getID + '/';
        console.log(link);
        /*set the form action*/
        $('#editFormHost').attr('action', link)
        $("#spanId").html(getID);
        //name selector $("input[name= ' '").val()    
        $('#roomNO').val(getRoomNO);
        $("input[name='cabinetNO']").val(getCabinetNO);
        $("input[name='bladeBoxNO']").val(getBladeBoxNO);
        $('#bladeNO').val(getBladeNO);
        $("input[name='hostName']").val(getHostName);
        $("input[name='serviceIP']").val(getServiceIP);
        $("input[name='manageIP']").val(getManageIP);
        $("input[name='storageIP']").val(getStorageIP);
        $("input[name='hardware']").val(getHardware);
        $("input[name='service']").val(getService);
        $("#clusterName option[text='12123']").attr("selected", true);
        // var options=$("#clusterName option:selected");
        // alert(options.val()); //拿到选中项的值
        // alert(options.text()); //拿到选中项的文本
        // alert(options.attr('url')); //拿到选中项的url值           
    }
};

/*         删除的模态*/
function toDeleteHost(id, e) {
    /*            获取当前点击事件标签上的id*/

    var getID = e.parentNode.parentNode.children[1].innerHTML;
    console.log("getid = " + getID)
    // document.body.onclick = function (event) { 部分浏览器不支持此方法，改用如上parentNode方式。
    //     var id = event.target.id;
    //     console.log(id);
    if (getID) {
        $.confirm({
            title: '删除如下主机?',
            content: '主机ID：' + getID,
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
                            url: "/host_delete/",
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
                                    var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                    $table.bootstrapTable('refresh', opt);
                                }
                                else {
                                    $.alert({
                                        title: '提示：',
                                        content: "主机ID：" + data[0] + " 正在使用，删除失败！",
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


//多个主机删除函数

function toBatchDeleteHost(id, e) {
    var rowObject = $("#mytable").bootstrapTable('getSelections');
    var row = JSON.stringify(rowObject);
    if (rowObject.length == 0) {
        $.alert({
            title: '提示：',
            content: '请先选择主机！',
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
            title: '删除如下主机?',
            content: '主机数量：' + rowObject.length,
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
                            url: "/batch_host_delete/",
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
                                        var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
                                        $table.bootstrapTable('refresh', opt);
                                    }
                                    else {
                                        $.alert({
                                            title: '提示：',
                                            content: "主机ID：" + newdata[0] + " 正在使用，删除失败！",
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
