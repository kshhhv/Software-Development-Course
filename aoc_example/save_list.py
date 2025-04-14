import numpy as np
import pickle
import json
from pathlib import Path

def save_list(the_list, file_path, file_format):

	if file_format == 'csv':
		np.savetxt(file_path.with_suffix('.csv'), the_list)

	if file_format == 'pickle':

		with open(file_path.with_suffix('.pkl'), 'wb') as f:
			pickle.dump(the_list, f)

	if file_format == 'json':

		with open(file_path.with_suffix('.json'), 'w') as f:
			json.dump(the_list, f)



if __name__ == '__main__':

	listis = [2,3,4,5]

	files_path = Path(".") / 'saved_list'


	save_list(listis, files_path, 'csv')
	save_list(listis, files_path, 'pickle')
	save_list(listis, files_path, 'json')