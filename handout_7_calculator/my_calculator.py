def run(inp_string):
	'''
	Does arithmetic operations

	Parameters
	----------
	inp_string: string
		Contains alternating numbers (int/float) and operators (+,-,x,/)

	Returns
	--------
	final_value: float
		
	'''

	# define supported operators
	operators = {'+', '-', '*', '/'}

	#list out of the input string
	inp_list = inp_string.split()


	i = 0
	while i < len(inp_list):

		item = inp_list[i]

		#skip over if it is not a defined operator
		if not (isinstance(item, str) and item in operators):
			i += 1
			continue


		try:
			# define the previous and next values on which operator will act
			if isinstance(item, str) and item in operators:
				prev = float(inp_list[i-1])
				nxt = float(inp_list[i+1])

			# calculate the values
			if item == '+':
				value = prev+nxt

			elif item == '-':
				value = prev-nxt

			elif item == '*':
				value = prev*nxt

			elif item == '/':
				value = prev/nxt

			else:
				raise ValueError("Unsupported operator")

			# delete that operator and the 2 values from the list
			del inp_list[i-1:i+2]

			#insert the new value
			inp_list.insert(i-1, str(value))

			#move back the index
			i -= 1


		except Exception as e:
			print(e)
		
		i += 1

		#if no more operations to do
		if len(inp_list) == 1: break

	final_value = float(inp_list[0])

	return final_value

if __name__ == '__main__':

	inp_string = '5 + 3 + 4 - 1'
	output = run(inp_string)

	print(output)

