from . import reverse_list
import itertools

def interleave(lista, listb):
	lista_reversed = reverse_list.reverse_list(lista)
	new_list = ''.join(list(itertools.chain(*zip(lista_reversed,listb))))
	return new_list