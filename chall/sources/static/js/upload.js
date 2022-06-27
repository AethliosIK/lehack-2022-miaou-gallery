// Notification handling
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

function callAPI(item) {
    var form = $("#" + item)[0];
    var file = $("#" + item + " #inputFile")[0];
    var data = new FormData();
    if (file.files.length != 0) {
        data.append("file", file.files[0]);
    }
    $.ajax({
        cache: false,
        type: form.method,
        url: form.action,
        data: data,
        processData: false,
        contentType: false,
        error: function(xhr, textStatus, error) {
            notify("danger", "An error occured [url=" + url + "] : "
                    + xhr.status + " " + error, 10000);
        },
        success: function(data) {
            notify(data.status, data.message);
        }
    });
}


$(document).on("click", "#upload-btn", function () {
    $("#upload-form").attr("action", "/api/upload");
    $("#upload-form").off("submit").submit(function(event) {
        event.preventDefault();
        return callAPI('upload-form');
    });
    $("#upload-form").submit();
});
