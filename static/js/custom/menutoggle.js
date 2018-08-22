/*Menu Toggle Script*/
       $("#menu-toggle").click(function(e) {
           	// 阻止浏览器默认动作 (页面跳转)
           e.preventDefault();
           $("#wrapper").toggleClass("toggled");
       });
