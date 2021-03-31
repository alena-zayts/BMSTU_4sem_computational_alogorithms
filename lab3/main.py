import numpy as np

# Таблица функции с количеством узлов N(11). Задать с помощью формулы
# y=x^2 в диапазоне [0..10] с шагом 1.
# [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81), (10, 100)]
def make_table(N=11):
    x = np.linspace(0, 10, N, dtype=int)
    y = x ** 2
    return {'x': x, 'y': y}

# создаем таблицу
data = make_table()
N = len(data['x'])

# находим hi
data['h'] = [None] + list(data['x'][i] - data['x'][i - 1]
                          for i in range(1, N))
# находим fi
data['f'] = [None, None] + list(3 * (((data['y'][i] - data['y'][i - 1]) / data['h'][i]) -
                                ((data['y'][i - 1] - data['y'][i - 2]) / data['h'][i - 1]))
                                for i in range(2, N))
# прямой ход: при известных кси2=0 и эта2=0, находим все прогоночные коэффициенты
data['xi'] = [None, None] + [0]
for i in range(3, N + 1):
    xi_i = -data['h'][i - 1] / (data['h'][i - 2] * data['xi'][i - 1] +
                     2 * (data['h'][i - 2] + data['h'][i - 1]))
    data['xi'].append(xi_i)

data['eta'] = [None, None] + [0]
for i in range(3, N + 1):
    eta_i = ((data['f'][i - 1] - data['h'][i - 2] * data['eta'][i - 1]) /
             (data['h'][i - 2] * data['xi'][i - 1] + 2 * (data['h'][i - 2] + data['h'][i - 1])))
    data['eta'].append(eta_i)

# обратные ход: при условии c[N+1]=0, определяем все коэффициенты c
# с помощью прогоночных коэффициентов
data['c'] = [None] + [0] * (N)
for i in range(N - 1, 0, -1):
    data['c'][i] = data['xi'][i + 1] * data['c'][i + 1] + data['eta'][i + 1]

# с помощью коэффициентов c находим коэффициенты b и d
data['b'] = [None] + list((data['y'][i] - data['y'][i - 1]) / data['h'][i] -
                          data['h'][i] * (data['c'][i + 1] - 2 * data['c'][i]) / 3
                          for i in range(1, N))

data['d'] = [None] + list((data['c'][i + 1] - data['c'][i]) / 3 / data['h'][i]
                          for i in range(1, N))

# находим все коэффициенты a из условия, что в узлах значения многочлена и интерполируемой функции совпадают
data['a'] = [None] + list(data['y'][i - 1] for i in range(1, N))


# поиск коэффициентов полинома на участке, в котором находится точка x
# а также точки, с которой начинается этот участок
def choose_coeffs(data, x):
    i_beg = 0
    for i in range(1, N - 1):
        if x < data['x'][i]:
            i_beg = i
            break
    return [data['a'][i_beg], data['b'][i_beg], data['c'][i_beg], data['d'][i_beg],
            data['x'][i_beg - 1]]

# подсчет значения полинома в точке x на участке, начинающемся с точки x0
def count_polynom3(a, b, c, d, x0, x):
    return (a + b * (x - x0) + c * (x - x0) ** 2 +
            d * (x -x0) ** 3)

# вводим значения x и интерполируем кубическим сплайном
x1 = 0.5
coeffs1 = choose_coeffs(data, x1)
res_spline1 = count_polynom3(*coeffs1, x1)

x2 = 5.5
coeffs2 = choose_coeffs(data, x2)
res_spline2 = count_polynom3(*coeffs2, x2)

# интерполируем полиномом Ньютона 3 степени (lab1.py - код из 1 ЛР)
import lab1
res_newton1 = lab1.approximate_newton(data['x'], data['y'], 3, x1)
res_newton2 = lab1.approximate_newton(data['x'], data['y'], 3, x2)

# подсчитываем настоящее значение
res_real1 = x1 ** 2
res_real2 = x2 ** 2

# вывод и сравнение результатов
print('Точка:', x1)
print('Интерполяция кубическим сплайном:', res_spline1)
print('Интерполяция полиномом Ньютона 3 степени:', res_newton1)
print('Настоящее значение:', res_real1)
print()

print('Точка:', x2)
print('Интерполяция кубическим сплайном:', res_spline2)
print('Интерполяция полиномом Ньютона 3 степени:', res_newton2)
print('Настоящее значение:', res_real2)


