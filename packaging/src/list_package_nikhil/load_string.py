def load_string(filename):
	with open(filename, "rb") as file:
		binary_data = file.read()
		string = binary_data.decode('utf-8')
		return string