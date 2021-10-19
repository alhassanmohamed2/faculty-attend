setInterval(function() {
    students_update();
}, 2000)

function students_update() {
    $.ajax({
        url: "/retrive-students",
        method: "POST",
        success: function(data) {
            $(".info").html(data)
        }
    })
}