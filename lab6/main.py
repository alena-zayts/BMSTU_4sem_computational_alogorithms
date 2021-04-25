import pandas as pd


def left_side_derivatives(x, y):
    derivatives = ['-']
    for i in range(1, len(y)):
        h = x[i] - x[i - 1]
        derivative = (y[i] - y[i - 1]) / h
        derivatives.append(derivative)
    return derivatives


def right_side_derivatives(x, y):
    derivatives = []
    for i in range(len(y) - 1):
        h = x[i + 1] - x[i]
        derivative = (y[i + 1] - y[i]) / h
        derivatives.append(derivative)
    derivatives.append('-')
    return derivatives


def central_derivatives(x, y):
    answer = ['-']
    for i in range(1, len(x) - 1):
        h = x[i + 1] - x[i - 1]
        answer.append((y[i + 1] - y[i - 1]) / h)
    answer.append('-')
    return answer


def runge_left_side_derivatives(x, y):
    answer = ['-', '-']

    for i in range(2, len(y)):
        f = (y[i] - y[i - 1]) / (x[i] - x[i - 1])
        s = (y[i] - y[i - 2]) / (x[i] - x[i - 2])
        answer.append(2 * f - s)

    return answer


def runge_right_side_derivatives(x, y):
    answer = []

    for i in range(len(y) - 2):
        f = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
        s = (y[i + 2] - y[i]) / (x[i + 2] - x[i])
        answer.append(2 * f - s)

    answer.append("-")
    answer.append("-")
    return answer


def align_vars_derivatives(x, y):
    answer = []

    for i in range(len(y) - 1):
        eta = (1 / y[i] - 1 / y[i + 1]) / (1 / x[i] - 1 / x[i + 1])
        answer.append(y[i] * y[i] * eta / (x[i] * x[i]))

    answer.append('-')
    return answer


def second_diff_derivatives(x, y):
    answer = ['-']

    for i in range(1, len(y) - 1):
        answer.append((y[i - 1] - 2 * y[i] + y[i + 1]) / (x[i] - x[i - 1]) ** 2)

    answer.append('-')
    return answer


def main():
    table = pd.DataFrame()
    table['x'] = [1, 2, 3, 4, 5, 6]
    table['y'] = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
    table['osd'] = left_side_derivatives(table['x'], table['y'])
    table.loc[0, 'osd'] = '%.3f *'%right_side_derivatives(table['x'], table['y'])[0]
    table['cd'] = central_derivatives(table['x'], table['y'])
    table['runge2'] = runge_left_side_derivatives(table['x'], table['y'])
    table.loc[0, 'runge2'] = '%.3f *' % runge_right_side_derivatives(table['x'], table['y'])[0]
    table.loc[1, 'runge2'] = '%.3f *' % runge_right_side_derivatives(table['x'], table['y'])[1]
    table['align'] = align_vars_derivatives(table['x'], table['y'])
    table['2dd'] = second_diff_derivatives(table['x'], table['y'])

    print(table)


if __name__ == "__main__":
    main()

