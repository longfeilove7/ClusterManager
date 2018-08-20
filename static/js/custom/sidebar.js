window.onload = function () /*to init open the sidebar*/ {
    $("#wrapper").toggleClass("toggled");
    /*to wait 1 second ,then resize the bootstrap-table */
    /*如果不固定表头不需要*/
    setTimeout(function () {
        $('#mytable').bootstrapTable('resetView');
    }, 1000);
}
/*to switch the sidebar*/
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    /*to wait 1 second ,then resize the bootstrap-table */
    /*如果不固定表头不需要*/
    setTimeout(function () {
        $('#mytable').bootstrapTable('resetView');
    }, 1000);
});