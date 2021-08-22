from flask import Flask, render_template, request, session
import sympy as sp
import numpy as np
import base64
from math import log, pi, sqrt
import time
from matplotlib.figure import Figure
from scipy.optimize import minimize_scalar, minimize
from io import BytesIO
# ініціалізація flask додатку
app = Flask(__name__)
# ініціалізація ключа для шифрування даних
app.secret_key = 'diploma work'
# створення списку з назвами першої змінної
var1 = ['x', 'z', 'u']
# створення списку з назвами першої змінної
var2 = ['t', 'y', 'v']


# функція для створення графіку наближення функції на певній ітерації
# на вхід отримує _i - номер ітерації та _plot - аналітичний вигляд функції, графік якої необхідно побудувати
def create_plot(_plot, _i):
    # отримання даних з сесії
    _x1 = session.get('x1')
    _x2 = session.get('x2')
    _a = session.get('a')
    _b = session.get('b')
    # визначення множника для побудови графіку
    if _a == 0:
        multiplier = _b
    else:
        multiplier = _a
    # створення списку значень незалежної змінної
    _x = np.linspace(_a - 0.1 * multiplier, _b + 0.1 * multiplier, 50)
    graph = Figure()
    ax = graph.subplots()
    # визначення заголовку графіку
    ax.set_title("Графік наближення".format(_i + 1))
    # визначення підпису для вісі х
    ax.set_xlabel(_x1)
    # визначення підпису для вісі у
    ax.set_ylabel('y(x)')
    # створення списку значень функції
    y_list = [sp.sympify(_plot).subs(_x1, k) for k in _x]
    # побудова графіку
    ax.plot(_x, y_list)
    return graph


# функція для побудови графіків розв'язку та наближень до нього
def create_figure():
    # отримання даних з сесії
    x1 = session.get('x1')
    x2 = session.get('x2')
    _a = session.get('a')
    _b = session.get('b')
    # перетворення рядків у клас бібліотеки Sympy для роботи з ними
    _x1 = sp.symbols(x1)
    _x2 = sp.symbols(x2)
    # отримання даних з сесії
    iters = session.get('functions')
    # визначення списку функцій, для яких будуть будуватися графіки
    _iterations = [sp.sympify(elem) for elem in iters]
    # визначення множника для побудови графіку
    # визначення списку значень незалежної змінної
    _x = np.linspace(_a, _b, 50)
    # створення фігури для графіків розв'язку та наближень на області їх визначення
    fig = Figure()
    ax = fig.subplots()
    # визначення заголовку графіку
    ax.set_title("Графік розв'язку та наближень до нього")
    # визначення підпису для вісі х
    ax.set_xlabel(str(_x1))
    # визначення підпису для вісі у
    ax.set_ylabel('y(x)')
    # скорочення списку відображених на графіку ітерацій до останніх 6
    if len(_iterations) > 5:
        _iterations = _iterations[-6:]
    for i in range(len(_iterations)):
        # створення списку значень функції
        y_list = [_iterations[i].subs(_x1, k) for k in _x]
        # створення списку, що має лише дійсні значення функції
        y_t = [float(elem) for elem in y_list if not isinstance(elem, sp.core.add.Add)]
        # знаходження різниці між довжинами списку
        short = len(_x) - len(y_t)
        _x = _x[short:]
        # побудова графіку
        ax.plot(_x, y_t, label="Ітерація №{}".format(i + 1))
    # додавання легенди
    ax.legend()
    return fig


# функція, що реалізує ітераційну процедуру стискаючих відображень
# функція отримує раньше підрахований коефіцієнт _alpha та відносну точність обчислень _delta
def picar(_alpha, _delta):
    # отримання даних з сесії
    x1 = session.get('x1')
    x2 = session.get('x2')
    _a = session.get('a')
    _b = session.get('b')
    _kernel = session.get('kernel')
    _func = session.get('func')
    _lamb = session.get('lamb')
    _delta = float(_delta)
    # перетворення рядків у клас бібліотеки Sympy для роботи з ними
    _x1 = sp.symbols(x1)
    _x2 = sp.symbols(x2)
    # побудова підінтегральної функції
    int_func = "(" + str(_kernel) + ")*(" + str(1) + ")"
    int_func_s = sp.sympify(int_func)
    # спрощення підінтегральної функції
    exp = sp.collect(int_func_s.expand(), [_x1, _x2])
    # інтегрування та множення на коефіцієнт лямбда
    try:
        integ = sp.sympify(_lamb) * sp.integrate(exp, (_x2, _a, _b))
    except sp.polys.polyerrors.PolynomialError:
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = \
            "Після інтегрування у наближенні до шуканої функції було виявлено логарифмічну функцію!"
        session['functions'] = []
        return 0, 0
    # знаходження наближення до функції
    y1 = integ + sp.sympify(_func)
    # спрощення знайденного наближення
    y1 = sp.collect(y1.expand(), [_x1, _x2])
    # перевірка на наявність логарифмічної функції у наближенні
    if 'log' in str(y1):
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = \
            "Після інтегрування у наближенні до шуканої функції було виявлено логарифмічну функцію!"
        session['functions'] = []
        return 0, 0
    # перевірка на наявність комплекснозначної функції у наближенні
    elif 'I' in str(y1):
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = "Після інтегрування у функції було виявлено комплексно-значну функцію!"
        session['functions'] = []
        return 0, 0

    # функція, що необхідна для знаходження коефіцієнта а за допомогою методів оптимізації
    def max1(x):
        # побудова максимуму модуля різниці між першою та нульовою ітераціями
        func3 = "-abs(" + str(_func) + "-" + str(y1) + ")"
        # заміна назви змінної на її значення
        func3 = func3.replace(str(_x1), str(x))
        return eval(func3)
    try:
        # знаходження максимуму модуля різниці між першою та нульовою ітераціями
        res = float(minimize_scalar(max1, bounds=(_a, _b), method='bounded').fun)
        # знаходження норми отриманого наближення
        x_norm = float(minimize_scalar(lambda x: eval("-abs(" + str(y1) + ")"), bounds=(_a, _b), method='bounded').fun)
    # первірка на ділення на нуль
    except ZeroDivisionError:
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = "У ході розв'язання рівняння було виявлено ділення на нуль."
        res = "err"
        x_norm = "err"
    if res == "err" or x_norm == "err":
        return 0, 0
    else:
        # домноження знайдених результатів на мінус для знаходження максимуму
        a = -1.0 * res
        norm = -1.0 * x_norm
    # обчислення відносної похибки
    delta_otn = _alpha * a / ((1 - _alpha) * norm)
    # визначення початкового значення критерія закінчення
    cond = True
    # перевірка критерія закінчення обчислень
    if _delta > delta_otn:
        cond = False
    # ініціалізація кількості ітерацій
    n = 1
    if session.get('int_funcs'):
        # видалення існуючих даних з сесії
        session.pop('functions')
        session.pop('int_funcs')
        session.pop('integrals')
        session.pop('delta_res')
    # створення списку для наближень до розв'язку
    functions = [str(y1)]
    # створення списку для підінтегральних функцій
    int_funcs = [str(exp)]
    # створення списку для проінтегрованих виразів
    integrals = [str(integ)]
    i = 1
    # ініціалізація часу початку обчислень
    tic = time.perf_counter()
    while cond:
        func = str(functions[i - 1]).replace(str(_x1), str(_x2))
        # побудова підінтегральної функції
        int_func = "(" + str(_kernel) + ")*(" + func + ")"
        int_func_s = sp.sympify(int_func)
        # спрощення підінтегральної функції
        exp = sp.collect(int_func_s.expand(), [_x1, _x2])
        int_funcs.append(str(exp))
        try:
            # інтегрування та множення на коефіцієнт лямбда
            integ = sp.sympify(_lamb) * sp.integrate(exp, (_x2, _a, _b))
        # перевірка на наявність можливих помилок при інтегруванні
        except (sp.polys.polyerrors.NotInvertible, sp.polys.polyerrors.PolynomialDivisionFailed):
            session['functions'] = []
            # видалення існуючого повідомлення про помилку з сесії
            session.pop('msg')
            # визначення відповідного повідомлення про помилку
            session['msg'] = \
                "Після інтегрування у наближенні до шуканої функції було виявлено функцію, що не є поліномом!"
            return 0, 0
        integrals.append(str(integ))
        # знаходження наближення до функції
        y1 = integ + sp.sympify(_func)
        # спрощення знайденного наближення
        y1 = sp.collect(y1.expand(), [_x1, _x2])
        try:
            # знаходження норми отриманого наближення
            x_norm = float(
                minimize_scalar(lambda x: eval("-abs(" + str(y1) + ")"), bounds=(_a, _b), method='bounded').fun)
        # перевірка на можливі помилки при знаходженні норми
        except (ZeroDivisionError, NameError):
            # видалення існуючого повідомлення про помилку з сесії
            session.pop('msg')
            # визначення відповідного повідомлення про помилку
            session['msg'] = "У ході розв'язання рівняння було виявлено ділення на нуль або введена функція " \
                             "не визначена на заданому інтервалі інтегрування!"
            x_norm = "err"
        if x_norm == "err":
            return 0, 0
        else:
            # множення знайденої на норми на мінус для знаходження максимуму
            norm = -1.0 * x_norm
        # обчислення відносної похибки
        delta_otn = (_alpha ** n) * a / ((1 - _alpha) * norm)
        # ініціалізація часу закічнення ітерація
        toc = time.perf_counter()
        # перевірка критерія закінчення обчислень
        if _delta > delta_otn:
            cond = False
        # перевірка на наявність логарифмічної функції у наближенні
        elif 'log' in str(y1):
            # видалення існуючого повідомлення про помилку з сесії
            session.pop('msg')
            # визначення відповідного повідомлення про помилку
            session['msg'] = \
                "Після інтегрування у наближенні до шуканої функції було виявлено логарифмічну функцію!"
            session['functions'] = []
            return 0, 0
        # перевірка на наявність комплекснозначної функції у наближенні
        elif 'I' in str(y1):
            # видалення існуючого повідомлення про помилку з сесії
            session.pop('msg')
            # визначення відповідного повідомлення про помилку
            session['msg'] = "Після інтегрування у функції було виявлено комплексно-значну функцію!"
            session['functions'] = []
            return 0, 0
        # перевірка часу обчислення
        elif int(toc - tic) > 15:
            # видалення існуючого повідомлення про помилку з сесії
            session.pop('msg')
            # визначення відповідного повідомлення про помилку
            session['msg'] = "Час обчислення вичерпався"
            session['functions'] = []
            # визначення останього наближення для його відображення на сторінці у вигляді формули
            lastf = sp.latex(sp.sympify(str(y1)))
            lastf = "\\displaylines{" + lastf + "}"
            # внесення даних до сесії
            session['last'] = [lastf, round(a, 5), round(n, 5), round(delta_otn, 5)]
            return 0, 0
        functions.append(str(y1))
        # перевірка, чи є отримане наближення точним аналітичним розв'язком
        if functions[i] == functions[i-1]:
            # визначення відносної похибку у випадку, коли знайдений розв'язкок є точним аналітичним розв'язком
            # введенного інтегрального рівняння
            session['delta_res'] = -1
            cond = False
        n += 1
        i += 1
    # перевірка на кількість виконаних ітерацій
    if n < 30:
        # внесення отриманих даних в сесію
        session['functions'] = functions
        session['int_funcs'] = int_funcs
        session['integrals'] = integrals
        # внесення результатів про відносну похибку до сесії
        # якщо був знайдений точний розв'язок, похибка не вноситься
        if session.get('delta_res') != -1:
            session['delta_res'] = delta_otn
    # якщо необхідно зробити більше 30 ітерацій
    else:
        # внесення даних, що були отримані на останній ітерації та "цукру"
        session['delta_res'] = delta_otn
        session['functions'] = [str(functions[i-1])]
        session['int_funcs'] = ['x']
        session['integrals'] = ['x']
    return a, n


# функція, що знаходить необхідні для розв'яку рівняння константи
# функція отримує відносну точність обчислень _delta
def parser(_delta):
    # отримання даних з сесії
    x1 = session.get('x1')
    x2 = session.get('x2')
    _a = session.get('a')
    _b = session.get('b')
    _kernel = session.get('kernel')
    _func = session.get('func')
    _lamb = session.get('lamb')
    # перетворення рядків у клас бібліотеки Sympy для роботи з ними
    _x1 = sp.symbols(x1)
    _x2 = sp.symbols(x2)

    # визначення функції, що ініціалізує аналітичний вигляд максимуму модуля ядра і необхідна для знаходження його
    # чисельного значення за допомогою методів оптимізації
    def max2(x):
        # побудова модуля ядра
        func3 = "-abs(" + str(_kernel) + ")"
        # заміна назви першої змінної на її значення
        func3 = func3.replace(str(_x1), str(x[0]))
        # перевірка на наявність слова sqrt в назві функції
        if func3.find('sqrt') != -1:
            return eval(func3)
        else:
            # заміна назви другої змінної на її значення
            func3 = func3.replace(str(_x2), str(x[1]))
            return eval(func3)
    _a = float(_a)
    _b = float(_b)
    try:
        # знаходження максимуму модуля ядра
        res = float(minimize(max2, np.array([_a, _b]), bounds=((_a, _b), (_a, _b)), method="Powell").fun)
    # перевірка на діленняя на нуль при знаходженні максимуму модуля ядра
    except (ZeroDivisionError, NameError):
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = "У ході розв'язання рівняння було виявлено ділення на нуль."
        res = "err"
    # перевірка на те, що введена функція визначена на вказаному користувачем відрізку
    except ValueError:
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = "Одна з введених функцій не визначена на введеному інтервалі інтегрування!"
        res = "err"
    if res == "err":
        session['functions'] = []
        return 0, 0, 0, 0
    else:
        # множення знайденого числа на мінус для знаходження максимуму
        m = -1.0 * res
    _lamb = abs(float(_lamb))
    # визначення коефіцієнта альфа
    alpha = m * _lamb * (_b - _a)
    # перевірка умов стиску інтегрального оператора
    if alpha >= 1:
        session['functions'] = []
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = "Коефіцієнт стиску \\(\\alpha \\) виявився більшим за 1!"
        return m, alpha, 0, 0
    # виклик функції, що реалізує ітераційну процедру стискаючих відображень
    a, n = picar(alpha, _delta)
    return m, alpha, a, n


# функція, що необхідна для валідації введених користувачем функцій
# на вхід вона отримує текстове представлення введеної функції text
def validation(text):
    # отримання даних з сесії
    x1 = session.get('x1')
    x2 = session.get('x2')
    # перетворення рядків у клас бібліотеки Sympy для роботи з ними
    _x1 = sp.symbols(x1)
    _x2 = sp.symbols(x2)
    # переведення рядка в нижній регістр
    text = text.lower()
    # заміна знаку ** підведення до степеня на знак ^
    text = text.replace('**', '^')
    # заміна ком на точки
    text = text.replace(',', '.')
    # знаходження довжини отриманого рядка
    text_len = len(text)
    i = 1
    while i < text_len:
        # отримання поточного символу рядку
        char1 = text[i - 1]
        # отримання попереднього символу рядку
        char2 = text[i]
        # перевірка наявності знака множення між назвами змінних
        if (char1 == str(_x1) or char1 == str(_x2)) and (char2 == str(_x1) or char2 == str(_x2)):
            # додавання символу множення в рядок для його правильного розпізнавання
            text = text[:i] + '*' + text[i:]
            # знаходження нової довжини рядка
            text_len = len(text)
        # перевірка на наявність показниково-степенової функції
        elif char1 == '^' and (char2 == str(_x1) or char2 == str(_x2)):
            return ''
        # перевірка на наявність показниково-степенової функції
        elif char1 == '^' and char2 == '(':
            # знаходження індексу дужки, що закриває степінь
            inx = text.find(')', i)
            # виділення підстроку степеня
            substr = text[i + 1:inx]
            # перевірка на наявність назви змінної в степені
            if substr.find('t') != -1 and substr.find('x') != -1:
                return ''
        i += 1
    # зворотня заміна знаку ^ підведення до степеня на знак **
    text = text.replace('^', '**')
    try:
        # спрощення введених функцій
        text = sp.sympify(text)
        text = sp.collect(text.expand(), [_x1, _x2])
        return str(text)
    # перевірка на наявність описок в введених функціях
    except sp.SympifyError:
        # видалення існуючого повідомлення про помилку з сесії
        session.pop('msg')
        # визначення відповідного повідомлення про помилку
        session['msg'] = "У введених функціях неправильно розставлені знаки арифметичних операцій або дужки."
        return ''


# функція для відображення сторінки з теоретичними відомостями за відповідним посилання
@app.route('/theory', methods=['GET'])
def theory():
    return render_template("theoretical.html")


# функція для відображення детального розв'язку інтегрального рівняння
@app.route('/solution', methods=['GET', 'POST'])
def solution():
    # отримання даних з сесії
    x1 = session.get('x1')
    x2 = session.get('x2')
    a = session.get('a')
    b = session.get('b')
    lamb = session.get('lamb')
    kernel = session.get('kernel')
    func = session.get('func')
    functions = session.get('functions')
    int_funcs = session.get('int_funcs')
    integrals = session.get('integrals')
    # формування списку аналітичних виразів наближень під знаком інтегралу
    functions_x2 = [elem.replace(str(x1), str(x2)) for elem in functions]
    # внесення початкового наближення до вищеозначеного списку
    functions_x2.insert(0, str(1))
    # знаходження довжини списку наближень
    n = len(functions)
    # ініціалізація списків для збереження функцій у вигляді формул
    funcs = []
    funcs2 = []
    integral_funcs = []
    int_list = []
    # визначення вільного члена у вигляді формули
    res_func = sp.latex(sp.sympify(func))
    res_func = "\\displaylines{" + res_func + "}"
    # визначення ядра у вигляді формули
    res_kern = sp.latex(sp.sympify(kernel))
    res_kern = "\\displaylines{" + res_kern + "}"
    funcs.append(res_func)
    # визначення наближень у вигляді формул
    for elem in functions:
        res = sp.latex(sp.sympify(elem))
        funcs.append("\\displaylines{" + res + "}")
    # визначення підінтегральних виразів у вигляді формул
    for elem in int_funcs:
        res = sp.latex(sp.sympify(elem))
        integral_funcs.append("\\displaylines{" + res + "}")
    # визначення проінтегрованих виразів у вигляді формул
    for elem in integrals:
        res = sp.latex(sp.sympify(elem))
        int_list.append("\\displaylines{" + res + "}")
    # визначення наближень під інтегралом у вигляді формул
    for elem in functions_x2:
        res = sp.latex(sp.sympify(elem))
        funcs2.append("\\displaylines{" + res + "}")
    # побудова графіків всіх наближень
    graphs = [create_plot(functions[i], i) for i in range(len(functions))]
    pict = []
    for i in range(len(graphs)):
        buf = BytesIO()
        # збереження графіку в буфер
        graphs[i].savefig(buf, format="png")
        # додавання графіку в список для відображення його на html сторінці
        pict.append(base64.b64encode(buf.getvalue()).decode("utf8"))
    return render_template("solution.html", functions=funcs, graphs=pict, a=a, b=b, kernel=res_kern, func=res_func,
                           lamb=lamb, x1=x1, x2=x2, n=n, int_funcs=integral_funcs, integrals=int_list,
                           funcs2=funcs2)


# функція для відображення головної сторінки додатку
@app.route('/', methods=['GET', 'POST'])
def index():
    # ініціалізації полів в сесії
    session['x1'] = ''
    session['x2'] = ''
    session['a'] = 0
    session['b'] = 0
    session['delta'] = 0
    session['delta_res'] = 0
    session['lamb'] = 0
    session['kernel'] = ''
    session['func'] = ''
    session['functions'] = []
    session['int_funcs'] = []
    session['integrals'] = []
    session['last'] = []
    session['msg'] = ''
    session['m'] = 0
    session['n'] = 0
    session['alpha'] = 0
    session['a_param'] = 0
    # відображення сторінки на get запитом
    if request.method == 'GET':
        return render_template("index.html", var1=var1, var2=var2, names=[var1[0], var2[0]])
    # відображення сторінки на post запитом
    else:
        # отримання даних з форми
        first = request.form['first']
        second = request.form['second']
        # видалення даних з сесії
        session.pop('x1')
        session.pop('x2')
        # занесення даних в сесію
        session['x1'] = first
        session['x2'] = second
        _names = [first, second]
        return render_template("index.html", var1=var1, var2=var2, names=_names)


# функція для відображення сторінки з результатами обчислень
@app.route('/data', methods=['GET', 'POST'])
def get_data():
    # відображення сторінки на post запитом
    if request.method == 'POST':
        # отримання даних з сесії
        x1 = session.get('x1')
        x2 = session.get('x2')
        # перетворення рядків у клас бібліотеки Sympy для роботи з ними
        _x1 = sp.symbols(x1)
        _x2 = sp.symbols(x2)
        # отримання даних з форми
        kernel = request.form['kernel']
        func = request.form['func']
        a = request.form['a']
        b = request.form['b']
        lamb = request.form['lambda']
        delta = request.form['delta']
        # видалення даних з сесії
        session.pop('a')
        session.pop('b')
        session.pop('delta')
        session.pop('lamb')
        session.pop('kernel')
        session.pop('func')
        # занесення отриманих з форми даних в сессію
        session['a'] = float(a)
        session['b'] = float(b)
        session['delta'] = float(delta)
        session['lamb'] = lamb
        # виклик функції для валідації введеного користувачем ядра інтегралнього рівняння
        check1 = validation(kernel)
        # виклик функції для валідації введеного користувачем вільного члена інтегралнього рівняння
        check2 = validation(func)
        # занесення результатів валідації в сесію
        session['kernel'] = check1
        session['func'] = check2
        # якщо користувач ввів правильні дані
        if check1 and check2:
            # виклик функції для обчислення важливих для процесу розвя'зку параметрів та подальший виклик функції
            # розв'язання інтегрального рівняння
            m, alpha, a_param, n = parser(delta)
            # занесення отриманих даних до сесії
            session['m'] = float(m)
            session['alpha'] = float(alpha)
            session['a_param'] = float(a_param)
            session['n'] = float(n)
            f_list = session.get('functions')
            func = sp.latex(sp.sympify(check2))
            kern = sp.latex(sp.sympify(check1))
            # округлення отриманих результатів
            alpha = round(alpha, 5)
            m = round(m, 5)
            # рівняння має розв'язок
            if len(f_list) > 0:
                # створення графіків розв'язків та наближень до них
                fig = create_figure()
                buf = BytesIO()
                fig.savefig(buf, format="png")
                figdata_png = base64.b64encode(buf.getvalue())
                _solution = True
                # визначення розв'язку у вигляді математичної формули
                ex1 = sp.sympify(f_list[-1])
                ex2 = ex1
                for k in sp.preorder_traversal(ex1):
                    if isinstance(k, sp.Float):
                        ex2 = ex2.subs(k, round(k, 5))
                result = sp.latex(sp.sympify(ex2))
                result = "\\displaylines{" + result + "}"
                # округлення отриманих результатів
                a_param = round(a_param, 5)
                delta_res = round(session.get('delta_res'), 5)
                return render_template("results.html", function=result, result=figdata_png.decode("utf8"), a=a, b=b,
                                       kernel=kern, func=func, lamb=lamb, x1=x1, x2=x2, m=m, alpha=alpha, delta=delta,
                                       a_param=a_param, n=n, sol=_solution, delta_res=delta_res)
            # введене рівняння не може бути розв'язане за допомогою методу стискаючих відображень
            else:
                # отримання повідомлення про помилку, що виникла
                msg = session.get('msg')
                _solution = False
                # отримання інформації про останнє наближення, що було знайдене без помилки
                last = session.get('last')
                return render_template("results.html", a=a, b=b, kernel=kern, func=func, lamb=lamb, x1=x1, x2=x2, m=m,
                                       alpha=alpha, delta=delta, sol=_solution, msg=msg, last=last)
        # користувач ввів неправильні дані
        else:
            # отримання повідомлення про помилку, що виникла
            msg = session.get('msg')
            return render_template("results.html", kernel=check1, func=check2, msg=msg)
    # відображення сторінки на get запитом
    else:
        # отримання даних з сесії
        x1 = session.get('x1')
        x2 = session.get('x2')
        # перетворення рядків у клас бібліотеки Sympy для роботи з ними
        _x1 = sp.symbols(x1)
        _x2 = sp.symbols(x2)
        # отримання даних з сесії
        kernel = session.get('kernel')
        func = session.get('func')
        a = session.get('a')
        b = session.get('b')
        lamb = session.get('lamb')
        delta = session.get('delta')
        delta_res = round(session.get('delta_res'), 5)
        # виклик функції для валідації введеного користувачем ядра інтегралнього рівняння
        check1 = validation(kernel)
        # виклик функції для валідації введеного користувачем вільного члена інтегралнього рівняння
        check2 = validation(func)
        # отримання даних з сесії
        m = session.get('m')
        alpha = session.get('alpha')
        a_param = session.get('a_param')
        n = session.get('n')
        f_list = session.get('functions')
        # визначення введених функцій у вигляді математичних формул
        func = sp.latex(sp.sympify(check2))
        kern = sp.latex(sp.sympify(check1))
        # округлення отриманих результатів
        alpha = round(alpha, 5)
        m = round(m, 5)
        # створення графіків розв'язків та наближень до них
        fig = create_figure()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        figdata_png = base64.b64encode(buf.getvalue())
        _solution = True
        # визначення розв'язку у вигляді математичної формули
        ex1 = sp.sympify(f_list[-1])
        ex2 = ex1
        for k in sp.preorder_traversal(ex1):
            if isinstance(k, sp.Float):
                ex2 = ex2.subs(k, round(k, 5))
        result = sp.latex(sp.sympify(ex2))
        result = "\\displaylines{" + result + "}"
        # округлення отриманих результатів
        a_param = round(a_param, 5)
        return render_template("results.html", function=result, result=figdata_png.decode("utf8"), a=a, b=b,
                               kernel=kern, func=func, lamb=lamb, x1=x1, x2=x2, m=m, alpha=alpha, delta=delta,
                               a_param=a_param, n=n, sol=_solution, delta_res=delta_res)


if __name__ == '__main__':
    app.run(debug=True)
