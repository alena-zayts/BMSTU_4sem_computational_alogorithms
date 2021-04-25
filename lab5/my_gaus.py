# поменять строки местами
def rows_swap(A, B, row1, row2):
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]

# поделить строку на число
def row_div(A, B, row, divider):
    A[row] = [a / divider for a in A[row]]
    B[row] /= divider

# сложить сстроку с другой, умноженной на число
def rows_sum(A, B, row, source_row, weight):
    A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
    B[row] += B[source_row] * weight

# решение системы методом Гаусса
def solve_gaus(A, B):
    column = 0
    while column < len(B):
        # Ищем максимальный по модулю элемент в column столбце
        current_row = None
        for r in range(column, len(A)):
            if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                 current_row = r
        if current_row is None:
            print("Ошибка: решений нет")
            return None

        if current_row != column:
            # Переставляем строку с найденным элементом наверх
            rows_swap(A, B, current_row, column)
        # Нормализуем строку с найденным элементом
        row_div(A, B, column, A[column][column])
        # Обрабатываем нижележащие строки
        for r in range(column + 1, len(A)):
            rows_sum(A, B, r, column, -A[r][column])
        column += 1
    # Матрица приведена к треугольному виду, считаем решение
    X = [0] * len(B)
    for i in range(len(B) - 1, -1, -1):
        X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))
    return X