   //     $(function(){
   //         //$('table tr:not(:first)').remove();
   //         var len = $('table tr').length;
   //         for(var i = 1;i<len;i++){
   //             $('table tr:eq('+i+') td:first').text(i);
   //         }

   // });
   function selectAll() {

       if ($("#select-all").is(":checked")) {

           $("[name='selected']").prop("checked", true);
           var allValue = queryCheckedValue();
       }
       else {

           $("[name='selected']").prop("checked", false);
       }

   }

   //获取所有选中checkbox的值

   function queryCheckedValue() {

       var arrayObj = new Array();

       $("input:checkbox[name='selected']:checked").each(function (i) {

           var val = $(this).val();

           arrayObj.push(val)
       });
    //控制台打印选中信息
       console.log(arrayObj)
       return arrayObj;

   }

   //所有的name为‘selected’的checkbox的值
   function noCheckedValue() {

       var str = "";
       $("input:checkbox[name='selected']").each(function (i) {

           var val = $(this).val();
           str = str + "," + val;
       });
       return str;
   }

   //判断所有的子checkbox全部选中时，总checkbox选中，否则，反之；
   function oneToAll() {

       var allChecked = 0;//所有选中checkbox的数量

       var all = 0;//所有checkbox的数量

       $("input:checkbox[name='selected']").each(function (i) {
           all++;
           if ($(this).is(":checked")) {
               allChecked++;
           }

       });

       if (allChecked == all) {//相等时，则所有的checkbox都选中了，否则，反之；

           $("#select-all").prop("checked", true);

       } else {

           $("#select-all").prop("checked", false);

       }

   }

   // $(function(){


   //     $("table tr").click(function(){
   //         var input = $(this).find("input[type=checkbox]");//获取checkbox    

   //         //判断当前checkbox是否为选中状态
   //         if(input.is(":checked")){           
   //             input.attr("checked",false);
   //         }else{
   //             input.attr("checked",true);
   //         }

   //     })  
   // })
