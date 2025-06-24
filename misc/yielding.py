def my_iter(num):
    c = num
    for ind in range(num - 1, 0, -1):
        c *= ind
        yield c
 
for x in my_iter(10):
    print(x)
 
print(type(my_iter(100)))

g = my_iter(2)
x = next(g)
print(f'{x=}')
x = next(g)