//表格监听函数,此函数用于服务器管理页面状态自动切换,由于ipmi.js为公用所以没在该脚本中时间动态更新数据
var $table = $('#mytable');
$table.on('load-success.bs.table column-switch.bs.table page-change.bs.table search.bs.table', function () {    
    $("table tr").each(function () {    // 遍历每一行
        var getID = $(this).children('td:eq(1)').text();//用text或html获取
        //alert(getID)
        // var getPowerOn = $(this).children('td:eq(13)').children().children().first();  // td:eq(0)选择器表示第一个单元格        
        // //console.log(getPowerOn)
        // var getPowerOff = $(this).children('td:eq(13)').children().children().eq(1);  // td:eq(0)选择器表示第一个单元格,eq() 方法返回被选元素中带有指定索引号的元素。        
        // //console.log(getPowerOff)
        // var getPowerCycle = $(this).children('td:eq(13)').children().children().last();   // td:eq(0)选择器表示第一个单元格        
        // //console.log(getPowerCycle)
        //var getPowerStatus = $(this).children('td:eq(15)').children().children().last();
        if (getID != undefined && getID != '') {
            var getPowerOn = $("#btn1_" + getID);
            //console.log(getPowerOn)
            var getPowerOff = $("#btn2_" + getID);
            //console.log(getPowerOff)
            var getPowerCycle = $("#btn3_" + getID);
            //console.log(getPowerCycle)
            var getPowerStatus = $("#btn4_" + getID);
            var getValue = getPowerOn.val();//.attr("value")和.val()都可以
            //console.log(getValue);
            //0:poweroff 1:poweron 2:powercycle
            if (getValue == 0) {
                getPowerOn.attr('disabled', false);
                getPowerOff.attr('disabled', true);
                getPowerCycle.attr('disabled', true);
                getPowerOn.children().css('color', 'yellowgreen');
                getPowerOff.children().css('color', 'grey');
                getPowerCycle.children().css('color', 'grey');
                getPowerStatus.children().css('color', 'grey');
                getPowerStatus.attr("title", "关机");
            }
            else if (getValue == 1) {
                getPowerOn.attr('disabled', true);
                getPowerOff.attr('disabled', false)
                getPowerCycle.attr('disabled', false);
                getPowerOn.children().css('color', 'grey');
                getPowerOff.children().css('color', 'yellowgreen');
                getPowerCycle.children().css('color', 'yellowgreen');
                getPowerStatus.children().css('color', 'green');
                getPowerStatus.attr("title", "开机");
            }
            else if (getValue == 2){
                getPowerOn.attr('disabled', true);
                getPowerOff.attr('disabled', true);
                getPowerCycle.attr('disabled', true);
                getPowerOn.children().css('color', 'grey');
                getPowerOff.children().css('color', 'grey');
                getPowerCycle.children().css('color', 'grey');
                getPowerStatus.children().css('color', 'red');
                getPowerStatus.attr("title", "IPMI故障");
            }
            else {
                getPowerOn.attr('disabled', false);
                getPowerOff.attr('disabled', false);
                getPowerCycle.attr('disabled', false);
                getPowerOn.children().css('color', 'yellowgreen');
                getPowerOff.children().css('color', 'yellowgreen');
                getPowerCycle.children().css('color', 'yellowgreen');
                getPowerStatus.children().css('color', '#921AFF');
                getPowerStatus.attr("title", "IPMI故障");
            }
        }
    });
});
