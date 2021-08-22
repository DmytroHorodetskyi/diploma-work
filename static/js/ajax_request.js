$(document).ready(function () {
    $("#name_form1").submit(function( event ) {
        // відправка запиту та попередження перезавантаження сторінки
        sendAjaxForm("name_form1", "msg");
        event.preventDefault();
    });
});
function sendAjaxForm(form_ajax, msg) {
    // отримання id форми
    var form = $("#" + "name_form1");
    // формування ajax-запиту
    $.ajax({
        // вказання типу запиту
        type: 'POST',
        url: '/',
        data: form.serialize(),
        // вказання відповіді у разі вдалого запиту
        success: function (response) {
            // отримання даних з форми
            var data = form.serialize();
            // розділення даних по знаку =
            var split = data.split("=");
            // виділення назви першої змінної
            var first = split[1][0];
            // виділення назви другої змінної
            var second = split[2];
            // формування рядку для відображення ядра на html-сторінці
            var k = "K(" + first + ", " + second + ")";
            // формування рядку для відображення вільного члена на html-сторінці
            var f = " &phi;(" + first + ")";
            var k_placeholer = first + "+" + second;
            var f_placeholer = first;
            // додавання отриманого виразу для ядра в html-сторінку
            $('#kern').text(k);
            // додавання отриманого виразу для вільного члена в html-сторінку
            $('#phi').html(f);
            $('#kernel_input').attr("placeholder", k_placeholer);
            $('#func_input').attr("placeholder", f_placeholer);
        },
        error: function (error) {
            // виведення повідомлення про помилку у випадку невдалого запиту
            console.log(error);
        }
    });
}