import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def logistic_map(x0, r, n):
	
	xs = [x0]

	for i in range(n-1):

		xn = xs[i]
		xnp1 = r*xn*(1-xn)

		xs.append(xnp1)

	return xs

if __name__ == '__main__':

	x_values = np.random.rand(100)
	n = 100

	r_values = np.linspace(0,4,100)


	x_values_ks = []

	xks = np.empty((100, 100, 100))


	for x_index, x in enumerate(x_values):

		for r_index, r in enumerate(r_values):
		
			xs = logistic_map(x, r, n)

			xks[x_index, r_index, :] = xs
		
	n = 3

	plt.plot(r_values, xks[1,:,0])
	plt.show()
	plt.plot(r_values, xks[1,:,1])
	plt.show()
	plt.plot(r_values, xks[1,:,2])
	plt.show()
	plt.plot(r_values, xks[1,:,3])
	plt.show()

	plt.plot(r_values, xks[50, :, n])
	plt.plot(r_values, xks[50, :, n+1])

	plt.show()


	plt.plot(range(100), xks[50,50,:])
	plt.show()
