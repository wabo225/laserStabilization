from wavelengthCorrection import getCorrection
from math import sqrt
correction = getCorrection(63.0245, 384_228.005)

resolution = correction(64.413338) - correction(64.416313)
resolution = - resolution
standardDeviation = resolution/sqrt(12)
print(f'{resolution=} GHz')
print(f'{standardDeviation=}')