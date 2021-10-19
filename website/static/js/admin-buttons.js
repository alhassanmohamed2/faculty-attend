$(document).on('click', 'button.attend', function() {

    $.ajax({
        url: "/attend-config",
        method: "POST",
        success: function(data) {
            $(".admin-action").html(data)
        }
    })
})
$(document).on('click', 'button.modify', function() {
    $.ajax({
        url: "/modify-students",
        method: "POST",
        success: function(data) {
            $(".admin-action").html(data)
        }
    })
})

$(document).on('click', 'button.search', function() {
    $.ajax({
        url: "/search-students",
        method: "POST",
        success: function(data) {
            $(".admin-action").html(data)
        }
    })
})


$(document).on('click', 'button.search_show', function() {
    name_student = $(".student_name").val()
    subject = $(".subject").val().replace('\n', "")
    dep = $(".departement").val().replace('\n', "")
    $.ajax({
        url: "/show_search_students",
        method: "POST",
        data: {
            name: name_student,
            subject: subject,
            dep: dep
        },
        success: function(data) {
            $("div.search").html(data)
        }
    })
})

$(document).on('click', 'button.stop', function() {
    $.ajax({
        url: "/stop-attend",
        method: "GET",
        success: function(data) {

        }
    })
})

$(document).on('click', 'button.start', function() {
    $.ajax({
        url: "/start-attend",
        method: "GET",
        success: function(data) {

        }
    })
})