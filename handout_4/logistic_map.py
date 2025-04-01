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
		
	fig, ax = plt.subplots()

	ax.set_xlim(min(r_values), max(r_values))
	ax.set_ylim(xks.min(), xks.max())

	def update(n):
	    ax.clear()
	    ax.set_title(f"N: {n}")  # Dynamic title

	    for x_index, x in enumerate(x_values):
	        ax.plot(r_values, xks[x_index, :, n], c='black')

	ani = animation.FuncAnimation(fig, update, frames=51, interval=100)

	plt.show()