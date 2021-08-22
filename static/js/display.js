// визначення функції для зміни вигляду форм при натиску на кнопку
document.getElementById("swap").onclick = function() {
    // зміна відображення форми для введення даних про інтегральне рівняння
    x = document.getElementById("form2");
    // відображення форми на сторінці
    x.style.visibility = "visible";
    x.style.position = "static";
    x.style.top = "auto";
    // зміна відображення форми для введення даних про назви змінних
    y = document.getElementById("form1");
    // видалення форми зі сторінки
    y.style.visibility = "hidden";
    y.style.position = "absolute";
    y.style.top = "-9999px";
}
// визначення функції для підказки у формі
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})