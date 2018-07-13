window.onload = function() /*to init open the sidebar*/
        {
            $("#wrapper").toggleClass("toggled");
        }
   
        $("#menu-toggle").click(function (e) {
            e.preventDefault();
            $("#wrapper").toggleClass("toggled");
        });