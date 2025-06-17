def save_string(filename, string):
	with open(filename, "wb") as file:
		file.write(string.encode('utf-8'))