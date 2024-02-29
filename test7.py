def multiply(x, flag):
    return x * 2

def sum1(x):
    return x + 1

elements = [1, 2, 3, 4]
elements_by2 = list(map(sum1, list(map( multiply, elements, True))))
print(elements_by2)
