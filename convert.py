import numpy as np
import pandas as pd
raw_file= 'test.dat'
with open(raw_file, "rb") as f:

      data_array = np.fromfile(f, dtype=np.int16)
      np.savetxt("test.csv", data_array, delimiter=',')

f.close()
