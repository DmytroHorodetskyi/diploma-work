// визначення змінної, що містить поле для введення ядра
var input1 = document.getElementById("kernel_input");
// визначення змінної, що містить поле для введення вільного члена
var input2 = document.getElementById("func_input");
// визначення змінної, що містить поле для введення параметра лямбда
var lambda = document.getElementById("lambda");
// визначення змінної, що містить поле для введення відносної точності
var delta_in = document.getElementById("delta_in");
// визначення змінної, що містить поле для введення правого кінця відрізку інтегрування
var a = document.getElementById("a");
// визначення змінної, що містить поле для введення лівого кінця відрізку інтегрування
var b = document.getElementById("b");
// функція, що робить лівий кінець відрізку інтегрування завжди меншим, ніж правий
function limit() {
	a.value=Math.min(b.value-0.01,a.value);
}
// функція, що прив'язана до поля введення лівого кінця відрізку інтегрування, та яка перевіряє правильність введених
// в дане поле даних
a.oninput = function() {
    // якщо дані правильні
    if (!a.checkValidity()) {
        // стилі відповідного поля змінюються на такі, що відображають правильне введення. Тобто зелений колір
        a.style.backgroundColor = "#FFCCCC";
        a.style.borderColor = "#FF9494";
        a.style.outline = "0";
        a.style.boxShadow = "inset 0 2px 2px #FFCCCC, 0 0 14px #FFCCCC";}
    // якщо дані неправильні
    else {
        // стилі відповідного поля змінюються на такі, що відображають неправильне введення. Тобто червоний колір
        a.style.backgroundColor = "#DFF2BF";
        a.style.borderColor = "#4BCA81";
        a.style.outline = "0";
        a.style.boxShadow = "inset 0 2px 2px #DFF2BF, 0 0 14px #DFF2BF";}}
// функція, що прив'язана до поля введення правого кінця відрізку інтегрування, та яка перевіряє правильність введених
// в дане поле даних
b.oninput = function() {
    // якщо дані правильні
    if (!b.checkValidity()) {
        // стилі відповідного поля змінюються на такі, що відображають правильне введення. Тобто зелений колір
        b.style.backgroundColor = "#FFCCCC";
        b.style.borderColor = "#FF9494";
        b.style.outline = "0";
        b.style.boxShadow = "inset 0 2px 2px #FFCCCC, 0 0 14px #FFCCCC";}
    // якщо дані неправильні
    else {
        // стилі відповідного поля змінюються на такі, що відображають неправильне введення. Тобто червоний колір
        b.style.backgroundColor = "#DFF2BF";
        b.style.borderColor = "#4BCA81";
        b.style.outline = "0";
        b.style.boxShadow = "inset 0 2px 2px #DFF2BF, 0 0 14px #DFF2BF";}}
// функція, що прив'язана до поля введення параметра лямбда, та яка перевіряє правильність введених
// в дане поле даних
lambda.oninput = function() {
    // якщо дані правильні
    if (!lambda.checkValidity()) {
        // стилі відповідного поля змінюються на такі, що відображають правильне введення. Тобто зелений колір
        lambda.style.backgroundColor = "#FFCCCC";
        lambda.style.borderColor = "#FF9494";
        lambda.style.outline = "0";
        lambda.style.boxShadow = "inset 0 2px 2px #FFCCCC, 0 0 14px #FFCCCC";}
    // якщо дані неправильні
    else {
        // стилі відповідного поля змінюються на такі, що відображають неправильне введення. Тобто червоний колір
        lambda.style.backgroundColor = "#DFF2BF";
        lambda.style.borderColor = "#4BCA81";
        lambda.style.outline = "0";
        lambda.style.boxShadow = "inset 0 2px 2px #DFF2BF, 0 0 14px #DFF2BF";}}
// функція, що прив'язана до поля введення відносної точності, та яка перевіряє правильність введених
// в дане поле даних
delta_in.oninput = function() {
    // якщо дані правильні
    if (!delta_in.checkValidity()) {
        // стилі відповідного поля змінюються на такі, що відображають правильне введення. Тобто зелений колір
        delta_in.style.backgroundColor = "#FFCCCC";
        delta_in.style.borderColor = "#FF9494";
        delta_in.style.outline = "0";
        delta_in.style.boxShadow = "inset 0 2px 2px #FFCCCC, 0 0 14px #FFCCCC";}
    // якщо дані неправильні
    else {
        // стилі відповідного поля змінюються на такі, що відображають неправильне введення. Тобто червоний колір
        delta_in.style.backgroundColor = "#DFF2BF";
        delta_in.style.borderColor = "#4BCA81";
        delta_in.style.outline = "0";
        delta_in.style.boxShadow = "inset 0 2px 2px #DFF2BF, 0 0 14px #DFF2BF";}}
// прив'язка функції limit до зміни полів для введенння кінців інтегрування
a.onchange=limit;
b.onchange=limit;
// функція, що прив'язана до поля введення ядра, та яка перевіряє правильність введених
// в дане поле даних
input1.oninput = function() {
    // визначення змінної, що містить значення поля для введення ядра
    var kernel = document.getElementById("kernel_input").value;
    // ініціалізація змінної, що містить патерн, який визначає правильний формат для даних, що вводяться
    var regstring = "[^"+val1+val2+"0-9*-/\\+\\^\\(\\) ]";
    kernel = kernel.replace(/\s+/g, ' ').trim();
    const regexp = new RegExp(regstring, "ig");
    var arr = kernel.match(regexp);
    const kern = document.getElementById("kernel_input");
    // визначення змінної, що містить блок, де буде розміщено повідомлення про можливу помилку
    var error1 = document.getElementById('smsg1')
    // визначення змінної, що містить кнопку, яка відправляє дані на сервер
    var button = document.getElementById('send');
    // якщо дані правильні
    if (arr!=null) {
        kern.style.backgroundColor = "#FFCCCC";
        kern.style.borderColor = "#FF9494";
        kern.style.outline = "0";
        kern.style.boxShadow = "inset 0 2px 2px #FFCCCC, 0 0 14px #FFCCCC";
        error1.textContent  = "Ви ввели неправильну функцію!";
        button.disabled = true;}
    // якщо дані неправильні
    else {
        kern.style.backgroundColor = "#DFF2BF";
        kern.style.borderColor = "#4BCA81";
        kern.style.outline = "0";
        kern.style.boxShadow = "inset 0 2px 2px #DFF2BF, 0 0 14px #DFF2BF";
        error1.textContent  = "";
        button.disabled = false;}};
// функція, що прив'язана до поля введення вільного члена, та яка перевіряє правильність введених
// в дане поле даних
input2.oninput = function() {
    // визначення змінної, що містить значення поля для введення вільного члена
    var func = document.getElementById("func_input").value;
    // ініціалізація змінної, що містить патерн, який визначає правильний формат для даних, що вводяться
    var regstring1 = "[^"+val1+"0-9*-/\\+\\^\\(\\) ]";
    func = func.replace(/\s+/g, ' ').trim();
    const regexp1 = new RegExp(regstring1, "ig");
    var arr1 = func.match(regexp1);
    const funcc = document.getElementById("func_input");
    // визначення змінної, що містить блок, де буде розміщено повідомлення про можливу помилку
    var error2 = document.getElementById('smsg2');
    // визначення змінної, що містить кнопку, яка відправляє дані на сервер
    var button = document.getElementById('send');
    // якщо дані правильні
    if (arr1!=null) {
        funcc.style.backgroundColor = "#FFCCCC";
        funcc.style.borderColor = "#FF9494";
        funcc.style.outline = "0";
        funcc.style.boxShadow = "inset 0 2px 2px #FFCCCC, 0 0 14px #FFCCCC";
        error2.textContent  = "Ви ввели неправильну функцію!";
        button.disabled = true;}
    // якщо дані неправильні
    else {
        funcc.style.backgroundColor = "#DFF2BF";
        funcc.style.borderColor = "#4BCA81";
        funcc.style.outline = "0";
        funcc.style.boxShadow = "inset 0 2px 2px #DFF2BF, 0 0 14px #DFF2BF";
        error2.textContent  = "";
        button.disabled = false;}};
// визначення змінної, що містить поле для вибору назви першої змінної
var first = document.getElementById("first");
// визначення змінної, що містить поле для вибору назви другої змінної
var second = document.getElementById("second");
// значення назви першої змінної за замовчуванням
var val1 = "x";
// значення назви другої змінної за замовчуванням
var val2 = "t";
first.onchange = function () {
    val1 = document.getElementById("first").value;
    val2= document.getElementById("second").value;}
second.onchange = function () {
    val1 = document.getElementById("first").value;
    val2 = document.getElementById("second").value;}