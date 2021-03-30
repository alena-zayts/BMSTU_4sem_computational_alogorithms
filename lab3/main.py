import numpy as np

# Таблица функции с количеством узлов N(11). Задать с помощью формулы
# y=x^2 в диапазоне [0..10] с шагом 1.
# [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81), (10, 100)]
def make_table(N=11):
    x = np.linspace(0, 10, N, dtype=int)
    y = x ** 2
    return {'x': x, 'y': y}

# найти кси(i+1)
def find_xi_iplus1(h_i, h_iminus1, xi_i):
    return (-h_i) / (h_iminus1 * xi_i +
                     2 * (h_iminus1 + h_i))

def find_eta_iplus1(f_i, h_):
    print()


data = make_table()
# i = [1, N - 1]
N = len(data['x'])
data['h'] = [None] + list(data['x'][i] - data['x'][i - 1]
                          for i in range(1, N))
# i = [2, N-1]
data['f'] = [None, None] + list(3 * (((data['y'][i] - data['y'][i - 1]) / data['h'][i]) -
                                ((data['y'][i - 1] - data['y'][i - 2]) / data['h'][i - 1]))
                                for i in range(2, N))
# i = [1, N-1]
data['a'] = [None] + list(data['x'][i - 1] for i in range(1, N))

# i = [2, N]
data['xi'] = [None, None] + [0]
for i in range(3, N + 1):
    xi_i = -data['h'][i - 1] / (data['h'][i - 2] * data['xi'][i - 1] +
                     2 * (data['h'][i - 2] + data['h'][i - 1]))
    data['xi'].append(xi_i)

# i = [2, N]
data['eta'] = [None, None] + [0]
for i in range(3, N + 1):
    eta_i = ((data['f'][i - 1] - data['h'][i - 2] * data['eta'][i - 1]) /
             (data['h'][i - 2] * data['xi'][i - 1] + 2 * (data['h'][i - 2] + data['h'][i - 1])))
    data['eta'].append(eta_i)

data['c'] = [None] + [0] * (N)
for i in range(N - 1, 0, -1):
    data['c'][i] = data['xi'][i + 1] * data['c'][i + 1] + data['eta'][i + 1]

#data['xi'] = ([None, None] + [0] +
#              list((-data['h'][i - 1]) / (data['h'][i - 2] * data['xi'][i - 1] +
#                     2 * (data['h'][i - 2] + data['h'][i - 1])) for i in range(3, N + 1)))
for l in data.values():
    print(l)


