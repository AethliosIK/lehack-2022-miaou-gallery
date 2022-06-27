function notify(type, message, delay=2000) {
    $.notify({
        message: $("<span>").text(message).html()
    },{
        delay: delay,
        type: type,
        placement: {
            from: "top",
            align: "center"
        }
    });
}

$(document).on("click", "#remove-image", function () {
    var item = $(".item.active")[0];
    var filename = item.children[0].id;
	var url = "/api/del?filename="+filename;
    if (filename != undefined) {
        $.get(url, function(data, status){
            notify(data.status, data.message);
        });
        setTimeout(function(){
            location.reload();
        }, 2000);
	}
});

