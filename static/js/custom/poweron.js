<script type="text/javascript">
      
// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

/** 
* 遍历表格内容返回数组
* @param Int  id 表格id
* @return Array
*/
function toPowerOn(id,e){
  var getID = e.parentNode.parentNode.children[0].innerHTML;
  var getIP = e.parentNode.parentNode.children[7].innerHTML;
  
  if(confirm("Power on "+ getIP)){
  $.ajax({
      contentType: "application/x-www-form-urlencoded; charset=utf-8",
      //contentType: "application/json; charset=utf-8", //django not support json,don't use this
      dataType: "json", //for to get json
      url : "/power_on/",
      type : "POST",
      cache : false,
      data : {
          'ID':getID, 
          'IP':getIP
            },       
      beforeSend: function (xhr, settings) {
      //此处调用刚刚加入的js方法
      var csrftoken = getCookie('csrftoken'); 
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      },
      success: function(data){                                                       
                          console.log(data)
                          //alert(data)
                          //以上是后端函数返回成功的信息
                          e.parentNode.parentNode.children[15].innerHTML=data[1]
                          if (data[2] == "fail"){
                              alert(data[0] + "poweron" + data[2])
                          }                            
                      },
      error: function(request,info,e){
                      alert("false");
                      console.log(e)
                      }
          })
      }
  }

</script>