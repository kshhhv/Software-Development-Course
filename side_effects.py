def func(x=[]):
	x.append('world!')
	print(x)


a = ['hello']
func(a)
func(a)

func()
func()