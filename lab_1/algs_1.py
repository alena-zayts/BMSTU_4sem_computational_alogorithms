from math import cos
import functions
import pandas as pd

def main():
    #исходные данные
    x = [0.00, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05]
    y = [1.000000, 0.838771, 0.655336, 0.450447,
         0.225336, -0.018310, -0.278390, -0.552430]
    yd = [-1.000000, -1.14944, -1.29552, -1.43497,
          -1.56464, -1.68164, -1.78333, -1.86742]
    n_range = range(1, 5)
    x0 = 0.525
    
    #получение результатов
    comp_table = []
    columns = ['n','y(x) по Ньютону', 'y(x) по Эрмиту', 'Вычисленный корень']
    for n in n_range:
        res_newton = functions.approximate_newton(x, y, n, x0)
        res_ermit = functions.approximate_ermit(x, y, yd, n, x0)
        root = functions.find_root_back_interp(x, y, n)
        comp_table.append([n, res_newton, res_ermit, root])
    
    #Вывод сравнительной таблицы
    print('Таблица для сравнения полиномов (x = 0.525, n - степень полинома)')
    df = pd.DataFrame(data = comp_table, columns = columns)
    df.index = df['n']
    df = df.drop('n', axis = 1)
    print(df)
    
if __name__ == "__main__":
    main()


  
   
print()
print('Примерное значение функции в данной точке: ', round(cos(x0) - x0, 6))
print('Примерное значение корня: ', 0.739)  

