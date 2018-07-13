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