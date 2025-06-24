import numpy as np
import matplotlib.pyplot as plt
from manual_image_registration import translation

data = np.load('hk122_0006.sr2.05.geometry.npz')

simulated = data['simulated_image']
observed = data['vic_data']

shift = translation.find_translate(observed, simulated)

print(shift)