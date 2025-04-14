from pathlib import Path
import numpy as np

files_path = Path(".") / "aoc2024-day1.txt"

data = np.loadtxt(files_path)

list_a = data[:,0]
list_b = data[:,1]

sorted_list_a = np.sort(list_a)
sorted_list_b = np.sort(list_b)

distance = 0 

for a,b in zip(sorted_list_a, sorted_list_b):
	distance += np.abs(a-b)

print(distance)