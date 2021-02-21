from copy import deepcopy


# Выбор узлов из данной таблицы nodes значений функций при значениях
# x в интервале x_values и y в интервале y_values для построения
# аппроксимирующего полинома степени n в точке (x0, y0)
# Возвращает таблицу выбранных узлов и соотвтествующие значения x и y
def choose_nodes(nodes, x_values, y_values, n, x0, y0):
    # необходимо выбрать n + 1 узлов
    need_to_take = n + 1
    if need_to_take > len(x_values):
        print('ОШИБКА: не хватает узлов')
    # находим узел, ближайший к значениям x0, y0
    x_closest_i = (sorted(range(len(x_values) - 1, -1, -1), key=lambda i: abs(x_values[i] - x0)))[0]
    y_closest_j = (sorted(range(len(y_values) - 1, -1, -1),
                          key=lambda j: abs(y_values[j] - y0)))[0]
    # определяем индексы необходимых узлов в исходной таблице
    # если не удается равномерно распределить узлы вокруг точки, выбираем из
    # того, что есть
    from_i = x_closest_i - need_to_take // 2
    if from_i < 0:
        from_i = 0
    to_i = from_i + need_to_take
    if to_i > len(x_values):
        to_i = len(x_values)
        from_i = to_i - need_to_take
    from_j = y_closest_j - need_to_take // 2
    if from_j < 0:
        from_j = 0
    to_j = from_j + need_to_take
    if to_j > len(y_values):
        to_j = len(y_values)
        from_j = to_j - need_to_take

    # формируем таблицу из выбранных узлов
    x_chosen = x_values[from_i:to_i]
    y_chosen = y_values[from_j:to_j]
    chosen_nodes = deepcopy(nodes)
    chosen_nodes = [row[from_j:to_j] for row in chosen_nodes[from_i:to_i]]

    return chosen_nodes, x_chosen, y_chosen


# Нахождение коэффициентов для одномерной аппроксимирующего полинома степени n
# по значениям функции func_values от значений переменной x_values
# Возвращает найденные коэффициенты
def find_coeffs(func_values, x_values, n):
    func_values = deepcopy(func_values)
    coeffs = [func_values[0]]
    # step - шаг (номер столбца в таблице после y)
    for step in range(n):
        # i - строка столбца
        for i in range(n - step):
            # вычисление разделенной разности для y от (step + 2) переменных
            func_values[i] = ((func_values[i + 1] - func_values[i]) /
                              (x_values[i + step + 1] - x_values[i]))
        coeffs.append(func_values[0])  # собираем значения из верхней строчки таблицы
    return coeffs


# Вычисление полинома степени n с коэффициентами coeffs
# по массиву переменной x в точке x0
# Возвращает значение полинома в точке x0
def count_polynom(x_values, coeffs, n, x0):
    summ = 0
    # вычисление очередного слагаемого
    for stage in range(n + 1):
        summand = coeffs[stage]
        for i in range(stage):
            summand *= (x0 - x_values[i])
        # Формирование ответа
        summ += summand
    return summ

# Интерполяция по x_values: находит f(x, yj), при  j = 0,1,..n
# Возвращает массив вычисленных f(x, yj), при  j = 0,1,..n
def interpolate_by_x(func_table, x_values, n, x0):
    func_arr = []
    # выполняем одномерную интерполяцию при выбранном значении yj
    for yj in range(n + 1):
        coeffs = find_coeffs([row[yj] for row in func_table], x_values, n)
        func_cur = count_polynom(x_values, coeffs, n, x0)
        func_arr.append(func_cur)
    return func_arr

# Интерполяция по y_values: по полученным значениям функции, привязанным к yj,
# интерполирует по y в точке y0
# Возвращает приближенное значение функции в точке (x0, y0)
def interpolate_by_y(func_array, y_values, n, y0):
    coeffs = find_coeffs(func_array, y_values, n)
    result = count_polynom(y_values, coeffs, n, y0)
    return result

def main():
    # исходные данные
    x_values = [0, 1, 2, 3, 4]
    y_values = [0, 1, 2, 3, 4]
    nodes = [[0, 1, 4, 9, 16],
             [1, 2, 5, 10, 17],
             [4, 5, 8, 13, 20],
             [9, 10, 13, 18, 25],
             [16, 17, 20, 25, 32]]
    x0 = 1.5
    y0 = 1.5
    n_range = [1, 2, 3]
    # выполнение задания
    answer_table = []
    # для степени полинома n
    for n in n_range:
        # выбираем необходимые узлы для интерполяции в точке (x0, y0)
        chosen_nodes, x_chosen, y_chosen = choose_nodes(nodes, x_values, y_values, n, x0, y0)
        # интерполируем по x
        func_array = interpolate_by_x(chosen_nodes, x_chosen, n, x0)
        # интерполируем по y
        answer = interpolate_by_y(func_array, y_chosen, n, y0)
        # заносим ответ в таблицу
        answer_table.append([n, answer])
    # выводим результаты
    for answer in answer_table:
        print('Степень полинома:', answer[0], '.Результат интерполяции:', answer[1])


if __name__ == "__main__":
    main()


