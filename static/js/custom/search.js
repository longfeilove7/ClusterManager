//for the old search
$(function () {
    $("#searchbox").keyup(function () {
        if ($(this).val() != "Search") {
            $("table tbody tr").hide()
                .filter(":contains('" + ($(this).val()) + "')").show();//filter and contains
        }

    }).keyup();
});
$("#searchbox").focus(function () {
    if ($(this).val() == "Search") {
        $(this).val("");
    }
}).blur(function () {
    if ($(this).val() == "") {
        $(this).val("Search");
    }
})


//for the bootstrap-select 
function selectOnChang(obj) {
    //获取被选中的option标签选项
    var value = $('#selectSearchBox').val()
    var strValue = JSON.stringify(value);
    alert(strValue);
    $.ajax({
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        //contentType: "application/json; charset=utf-8", //django not support json,don't use this
        dataType: "json", //for to get json
        url: "/host_info_query/",
        type: "POST",
        cache: false,
        data: {
            'allValue': strValue
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
            var opt = { url: "/host_info_query/?format=json", silent: true, query: { type: 1, level: 2 } }
            $table.bootstrapTable('refresh', opt);

            //以上是后端函数返回成功的信息
        },
        error: function (request, info, e) {
            alert("false");
            console.log(e)
        }
    })
}
