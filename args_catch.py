def func(*args, **kwargs):
	print(args)
	print(kwargs)

a = (1,2,3)
func(*a)

print(ord('h'))


d = {"a": 3.14, "b": 42, "c": 1}
 
# Iterating a dict iterates the keys
for c in d:
    print(c)
 
# dict.items return a iterable of tuples with both keys and values
for item in d.items():
    print(f"{item[0]}={item[1]}")
 
# multiple variable assignment in loops too!
for key, value in d.items():
    print(f"{key}={value}")