import numpy as np
from math import cos, sin, exp, pi
from my_gaus import solve_gaus
import matplotlib.pyplot as plt

EPS = 1e-6


# коэффициенты полинома Лежандра степени n
def make_legender_polynom(n):
    assert(n >= 0)

    if n == 0:
        coeffs = [1]
    elif n == 1:
        coeffs = [0, 1]
    else:
        coeffs = [0]
        coeffs_minus1 = make_legender_polynom(n - 1)
        mult1 = (2 * n - 1) / n
        coeffs_minus2 = make_legender_polynom(n - 2)
        mult2 = -(n - 1) / n
        for coeff in coeffs_minus1:
            coeffs.append(coeff * mult1)
        for i in range(n-1):
            coeffs[i] += coeffs_minus2[i] * mult2
    return coeffs


# вычисление полинома в точке x
def count_polynom(coeffs, x):
    y = 0
    for i in range(len(coeffs)):
        y += coeffs[i] * (x ** i)
    return y


# нахождениие корня методом половинного деления
def find_root_hdm(coeffs, a, b):
    while abs(b - a) > EPS:
        x = (b + a) / 2.0
        if count_polynom(coeffs, a) * count_polynom(coeffs, x) < 0:
            b = x
        else:
            a = x
    if abs(count_polynom(coeffs, x)) < EPS*10:
        return x


# корни полинома Лежандра степени n
def find_roots_legender_polynom(n):
    assert(n > 0)

    coeffs = make_legender_polynom(n)
    roots = []

    if n % 2:
        roots.append(0)

    step = 1. / (n+1)
    a = 0
    b = step

    while len(roots) < n:
        root = find_root_hdm(coeffs, a, b)
        if root and (root not in roots):
            roots.append(root)
            roots.append(-root)
        a = b
        b += step

    return sorted(roots)


# нахождение весов квадратур Гаусса
def find_gaus_weights(roots):
    matrix = []
    answers = []
    for i in range(len(roots)):
        line = np.array(roots) ** i
        if i % 2:
            answer = 0
        else:
            answer = 2. / (i + 1)

        answers.append(answer)
        matrix.append(line)
    # solve_gaus - решение СЛАУ методом Гаусса, реализация приводилась
    # в предыдущих лабораторных
    return solve_gaus(matrix, answers)


# интегрирование методом Гаусса
def integrate_gaus(func, n, a, b):
    roots = np.array(find_roots_legender_polynom(n))
    roots_scaled = ((b + a) / 2) + roots * ((b - a) / 2)
    vectorized_func = np.vectorize(func)
    function_values = vectorized_func(roots_scaled)
    weights = np.array(find_gaus_weights(roots))
    answer = sum(function_values * weights) * ((b - a) / 2)
    return answer


# интегрирование методом Симпсона
def integrate_simpson(func, n, a, b):
    h = float(b - a) / (n - 1)
    x = a
    answer = 0
    for i in range((n - 1) // 2):
        answer += func(x) + 4 * func(x + h) + func(x + 2 * h)
        x += 2 * h
    answer *= (h / 3)
    return answer


# перевод функции от двух переменных в функцию от одной переменной
def reform_21(func2, fixed):
    return lambda x: func2(fixed, x)


# вычисление двукратного интеграла
def tf_integrate(func, limits, ns, methods):
    Func = lambda x: methods[1](reform_21(func, x), ns[1], limits[1][0], limits[1][1])
    return methods[0](Func, ns[0], limits[0][0], limits[0][1])


# создание функции для для вычисления двукратного интеграла
def make_func_to_count(tau):
    l_r = lambda teta, phi: 2 * cos(teta) / (1 - (sin(teta) ** 2) * (cos(phi) ** 2))
    func = lambda teta, phi: (4 / pi) * (1 - exp(-tau * l_r(teta, phi))) * cos(teta) * sin(teta)
    return func


# выполнение задания при фиксированном тау и количествах узлов
def main_count(tau, n1, n2):
    func = make_func_to_count(tau)
    return tf_integrate(func, [[0, pi / 2], [0, pi / 2]], [n1, n2], [integrate_gaus, integrate_simpson])


def comare_ns():
    tau = 1
    ns_g = [3, 5, 7, 9, 11]
    ns_s = [6, 10,  14]
    plt.figure(figsize=(7, 7))
    plt.rcParams['font.size'] = '12'
    plt.title('Влияние количества выбираемых узлов на точность расчетов')
    plt.xlabel('n_s')
    plt.ylabel('answer')
    plt.grid()
    m = []
    for n_g in ns_g:
        y = []
        for n_s in ns_s:
            answer = main_count(tau, n_g, n_s)
            y.append(answer)
        m.append(y)

    for i in range(len(m)):
        plt.plot(ns_s, m[i], label='n_g=%d' % (ns_g[i]))
    plt.legend(loc='best')
    plt.show()

    plt.figure(figsize=(7, 7))
    plt.rcParams['font.size'] = '12'
    plt.title('Влияние количества выбираемых узлов на точность расчетов')
    plt.xlabel('n_g')
    plt.ylabel('answer')
    plt.grid()
    m = []
    for n_s in ns_s:
        y = []
        for n_g in ns_g:
            answer = main_count(tau, n_g, n_s)
            y.append(answer)
        m.append(y)

    for i in range(len(m)):
        plt.plot(ns_g, m[i], label='n_s=%d' % (ns_s[i]))
    plt.legend(loc='best')
    plt.show()


def compare_tau():
    n_s = n_g = 5
    plt.figure(figsize=(7, 7))
    plt.rcParams['font.size'] = '12'
    plt.title('epsilon(tau)')
    plt.xlabel('tau')
    plt.ylabel('epsilon')
    plt.grid()
    answers = []

    taus = np.linspace(0.05, 10)
    for tau in taus:
        answer = main_count(tau, n_g, n_s)
        answers.append(answer)

    plt.plot(taus, answers)
    plt.show()


def main():
    compare_tau()
    comare_ns()


if __name__ == '__main__':
    main()
