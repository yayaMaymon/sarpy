# scripts/example.py

# %%
import sarpy
from sarpy.io.complex.nisar import NISARReader
from sarpy.io.complex.converter import open_complex
from matplotlib import pyplot
from sarpy.visualization.remap import Density

print("SarPy version:", sarpy.__version__)
# nisar_file_path = '/Users/user/Documents/GitHub/NiSarData/NISAR_L1_PR_RSLC_001_030_A_019_2000_SHNA_A_20081012T060910_20081012T060926_D00402_N_F_J_001.h5'
filePath = '/Users/user/Downloads/sicd_example_1_PFA_RE32F_IM32F_HH.nitf'
reader = open_complex(filePath)
remap_function = Density()
# show the initial 500 x 500 chip, using the "standard" remap
chip = reader[:, :]
chip_display = remap_function(chip)
fig, axs = pyplot.subplots(nrows=1, ncols=1, figsize=(5, 5))
axs.imshow(chip_display, cmap='gray')
pyplot.show()


a = 1
# Just an example. Replace with real NISAR file path if you have it.
# nisar_file_path = '/path/to/your/NISAR/file.h5'
# reader = NISARReader(nisar_file_path)
# Do some processing...


# %%
