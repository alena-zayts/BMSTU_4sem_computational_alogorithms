#Синхронная сортировка двух массивов по возрастанию элементов в первом
#Возвращает отсортированные массивы
def sync_sort2(x, y):
    indices = sorted(range(len(x)), key=lambda i: x[i])
    x = [x[i] for i in indices]
    y = [y[i] for i in indices]
    return x, y

#Синхронная сортировка трех массивов по возрастанию элементов в первом
#Возвращает отсортированные массивы
def sync_sort3(x, y, yd):
    indices = sorted(range(len(x)), key=lambda i: x[i])
    x = [x[i] for i in indices]
    y = [y[i] for i in indices]
    yd = [yd[i] for i in indices]
    return x, y, yd

#Выбор узлов из массивов x, y для полинома Ньютона степени n и вычисления y(x0)
#Возвращает массивы выбранных узлов
def prepare_arrays_newton(x, y, n, x0):
    #необходимо выбрать n + 1 узлов
    need_to_take = n + 1
    if need_to_take > len(x):
        print('ОШИБКА: не хватает точек для построения полинома Ньютона')
    #сортируем (чтобы верно выбрать ближайшие узлы)
    x, y = sync_sort2(x, y)
    #находим точку в таблице, которая ближе всего к x0, 
    #чтобы выбирать узлы вокруг неё
    closest_to_x0_i = (sorted(range(len(x)), key=lambda i: abs(x[i] - x0)))[0]
    #определяем индексы необходимых узлов в исходных массивах
    #если не удаетсся равномерно распределить узлы вокруг точки, выбираем из
    #того, что есть
    from_i = closest_to_x0_i - need_to_take // 2 
    if from_i < 0:
        from_i = 0   
    to_i = from_i + need_to_take 
    if to_i > len(x):
        to_i = len(x)
        from_i = to_i - need_to_take
    #формируем массивы из выбранных узлов    
    x_new = x[from_i : to_i]
    y_new = y[from_i : to_i]
    return x_new, y_new

#Выбор узлов из массивов x, y, yd для полинома Эрмита степени n и вычисления y(x0)
#Возвращает массивы выбранных узлов
def prepare_arrays_ermit(x, y, yd, n, x0):
    #при построении полинома Эрмита используются как значения функции, так и 
    #значения производных, поэтому необходимое количество точек вычисляется так
    need_to_take = (n // 2) + 1
    if need_to_take > len(x):
        print('ОШИБКА: не хватает точек для построения полинома Эрмита')
    #сортируем (чтобы верно выбрать ближайшие узлы)
    x, y, yd = sync_sort3(x, y, yd)
    #находим точку в таблице, которая ближе всего к x0, 
    #чтобы выбирать узлы вокруг неё
    closest_to_x0_i = (sorted(range(len(x)), key=lambda i: abs(x[i] - x0)))[0]
    #определяем индексы необходимых узлов в исходных массивах
    #если не удаетсся равномерно распределить узлы вокруг точки, выбираем из
    #того, что есть
    from_i = closest_to_x0_i - need_to_take // 2 
    if from_i < 0:
        from_i = 0   
    to_i = from_i + need_to_take
    if to_i > len(x):
        to_i = len(x)
        from_i = to_i - need_to_take
    #формируем массивы из выбранных узлов
    #при этом таблицу из x, y преобразуем к виду, удобному для отыскания
    #разделенных разностей согласно процедуре обработки полинома Ньютона.
    x_new = []
    y_new = []
    yd_new = []
    for i in range(from_i, to_i):
        x_new.append(x[i])
        x_new.append(x[i])
        y_new.append(y[i])
        y_new.append(y[i])
        yd_new.append(yd[i])
    return x_new, y_new, yd_new

#Поиск коэффициентов для интерполяционного полинома Ньютона n-й степени
#с использованием масивов узлов x, y
#Возвращает массив коэффициентов
def find_coeffs_newton(x, y, n):
    coeffs = [y[0]] #первое слагаемое - y(x[0])
    #step - шаг (номер столбца в таблице после y)
    for step in range(n):
        #i - строка столбца
        for i in range(n - step):
            #вычисление разделенной разности для y от (step + 2) переменных
            y[i] = (y[i + 1] - y[i])/(x[i + step + 1] - x[i]) 
        coeffs.append(y[0])
    return coeffs

#Поиск коэффициентов для интерполяционного полинома Эрмита n-й степени
#с использованием масивов узлов x, y, yd
#Формально строим полином Ньютона по (n // 2) + 1 узлам, каждый из которых 
#повторяется дважды
#Возвращает массив коэффициентов
def find_coeffs_ermit(x, y, yd, n):
    coeffs = [y[0]] #первое слагаемое - y(x[0])
    #step - шаг (номер столбца в таблице после y)
    for step in range(n):
        #i - строка столбца
        for i in range(n - step):
            #вычисление разделенной разности для y от (step + 2) переменных
            #на нулевом шаге (кратность 2) формулы для разделенных разностей 
            #получаются предельным переходом
            if (step == 0) and (i % 2 == 0):
                y[i] = yd[i // 2]
            else:
                y[i] = (y[i + 1] - y[i])/(x[i + step + 1] - x[i])
        coeffs.append(y[0])
    return coeffs

#Вычисление полинома степени n с коэффициентами coeffs по массиву x в точке x0
#Возвращает значение полинома в точке x0
def count_polynom(x, coeffs, n, x0):
    summ = 0
    #вычисление очередного слагаемого
    for stage in range(n + 1):
        summand = coeffs[stage]
        for i in range(stage):
            summand *= (x0 - x[i])
        #Формирование ответа
        summ += summand
    return summ

#Приближенное вычисление y(x0) c помощью полинома Ньютона n-й степени
#(объединение функций prepare_arrays_newton,find_coeffs_newton и count_polynom) 
#Возвращает значение полинома Ньютона в точке x0   
def approximate_newton(x, y, n, x0):
    x_newton, y_newton = prepare_arrays_newton(x, y, n, x0)
    coeffs = find_coeffs_newton(x_newton, y_newton, n)
    return count_polynom(x_newton, coeffs, n, x0)

#Нахожление корня функции с помощью обратной интерполяции 
#используя полином Ньютона.
def find_root_back_interp(x, y, n):
    return approximate_newton(y, x, n, 0)

#Приближенное вычисление y(x0) c помощью полинома Эрмита n-й степени
#(объединение функций prepare_arrays_ermit,find_coeffs_ermit и count_polynom) 
#Возвращает значение полинома Эрмита в точке x0   
def approximate_ermit(x, y, yd, n, x0):
    x_ermit, y_ermit, yd_ermit = prepare_arrays_ermit(x, y, yd, n, x0)
    coeffs = find_coeffs_ermit(x_ermit, y_ermit, yd_ermit, n)
    return count_polynom(x_ermit, coeffs, n, x0)
