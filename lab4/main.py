import numpy as np
import pandas as pd  # для работы с таблицами
import my_gaus  # реализация решения системы методом Гаусса
import matplotlib.pyplot as plt  # для графиков


# таблица по умолчанию: x принимает значения [1, N] с шагом 1
# y - случайные значения на отрезке [1, N * 2]
# p - веса - все равны 1
def make_table(N):
    np.random.seed(1)
    x = np.linspace(1, N, N, dtype=int)
    y = np.random.randint(1, N * 2 + 1, N)
    p = np.array([1] * N)
    return x, y, p


# формирование левой части СЛАУ
def find_left_part(n, N, x, p):
    matrix = []
    for k in range(n + 1):
        row = []
        for m in range(n + 1):
            coeff = 0
            for i in range(N):
                coeff += p[i] * (x[i] ** (k + m))
            row.append(coeff)
        matrix.append(row)

    return matrix


# формирование правой части СЛАУ
def find_right_part(n, N, x, y, p):
    coeffs = []
    for k in range(n + 1):
        coeff = 0
        for i in range(N):
            coeff += p[i] * y[i] * (x[i] ** k)
        coeffs.append(coeff)
    return coeffs


# вычисление y с помошью коэффициентов полинома
def count_polynom(coeffs, x):
    y = []
    for x_cur in x:
        y_cur = 0
        for i in range(len(coeffs)):
            y_cur += coeffs[i] * (x_cur ** i)
        y.append(y_cur)
    return y


# Вывод таблицы
def output_table(x, y, p):
    print('Таблица:')
    df = pd.DataFrame(data=zip(x, y, p),
                      columns=['x', 'y', 'p'])
    print(df)

# Отрисовка графиков
def plot_polynoms1(x, y, polynoms):
    plt.figure(figsize=(7, 7))
    plt.rcParams['font.size'] = '12'
    plt.title('Аппроксимация функции методом наименьших квадратов')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()

    plt.scatter(x, y, label='dots')
    for i in range(len(polynoms)):
        plt.plot(x, count_polynom(polynoms[i], x), label='n=%d'%(i+1))

    plt.legend(loc='best')
    plt.show()


def plot_polynoms2(x, y, polynoms):
    plt.figure(figsize=(7, 7))
    plt.rcParams['font.size'] = '12'
    plt.title('Аппроксимация функции методом наименьших квадратов')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()

    plt.scatter(x, y, label='dots')
    plt.plot(x, count_polynom(polynoms[0], x), label='pi=1')
    plt.plot(x, count_polynom(polynoms[1], x), label='pi изменены')

    plt.legend(loc='best')
    plt.show()


# первое задание
def task_1():
    N = 5  # количество узлов
    # создаем таблицу, где все веса равны 1
    x, y, p = make_table(N)
    n_min = 1
    n_max = 4  # максимальная степень полинома
    polynoms = []  # массив для хранения полиномов
    for n in range(n_min, n_max + 1):
        # формируем левую и правую части СЛАУ
        A = find_left_part(n, N, x, p)
        B = find_right_part(n, N, x, y, p)
        # находим решение методом Гаусса
        coeffs = my_gaus.solve_gaus(A, B)
        polynoms.append(coeffs)
    print('Все веса равны 1')
    output_table(x, y, p)
    plot_polynoms1(x, y, polynoms)

# второе задание
def task_2():
    N = 5  # количество узлов
    # создаем таблицу, где все веса равны 1
    x, y, p1 = make_table(N)
    p2 = [10, 1, 10, 1, 1]
    n = 1  # степень полинома
    polynoms = []  # массив для хранения полиномов
    for p in [p1, p2]:
        # формируем левую и правую части СЛАУ
        A = find_left_part(n, N, x, p)
        B = find_right_part(n, N, x, y, p)
        # находим решение методом Гаусса
        coeffs = my_gaus.solve_gaus(A, B)
        polynoms.append(coeffs)
    print('Все веса равны 1')
    output_table(x, y, p1)

    print('Измененные веса')
    output_table(x, y, p2)
    plot_polynoms2(x, y, polynoms)


def main():
    task_1()
    task_2()


if __name__ == '__main__':
    main()