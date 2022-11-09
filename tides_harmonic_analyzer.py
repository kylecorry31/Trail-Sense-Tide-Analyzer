import matplotlib.pyplot as plt
import math
import datetime
import pytz

input_file = open('tides.csv', 'r')

EST = pytz.timezone('US/Eastern')
UTC = pytz.timezone('GMT')
start = datetime.datetime(2022, 1, 1, tzinfo=EST)
start_delta = (start - datetime.datetime(2021, 1, 1, tzinfo=UTC)).total_seconds() / 3600

d = list(map(float, input_file.read().split(',')))
# d = list(map(lambda line: float(line.split(',')[1]), input_file.readlines()[1:]))
input_file.close()

# TODO Use the times in the CSV file
# TODO Convert the phases to be relative to Jan 1 of the year in UTC

x = [i/60 + start_delta for i in range(len(d))]
# d = [math.cos(5 * i) + 0.5 * math.cos(12 * i) for i in x]

def get_harmonic(f, x, y, offset):
    cos = 0
    sin = 0
    x_range = x[-1] - x[0]
    dx = x_range / len(x)
    for i in range(len(x)):
        psin = y[i] * math.sin(f * x[i])
        pcos = y[i] * math.cos(f * x[i])
        cos += pcos * dx
        sin -= psin * dx
    sin *= 2 / x_range
    cos *= 2 / x_range

    phase = offset - math.degrees(math.atan2(sin, cos))
    amplitude = math.hypot(sin, cos)

    return (f, amplitude, phase)


def get_wave(harmonics, x, offsets):
    wave = []
    for i in range(len(x)):
        total = 0
        for j in range(len(harmonics)):
            h = harmonics[j]
            offset = offsets[j]
            total += h[1] * math.cos(h[0] * x[i] + math.radians(offset) - math.radians(h[2]))
        wave.append(total)
    return wave

def subtract(y, wave):
    return [y[i] - wave[i] for i in range(len(y))]

original = d

frequencies = [
    math.radians(28.984104),
    math.radians(30),
    math.radians(28.43973),
    math.radians(15.041069),
    math.radians(57.96821),
    math.radians(13.943035),
    math.radians(14.958931),
    math.radians(29.528479),
    math.radians(30.082138),
    math.radians(58.984104)
]

# TODO: Create a lookup table for offsets by year
# offsets = [ # This is for 2021
#     304.098,
#     0.138,
#     33.743,
#     2.518,
#     248.196,
#     304.678,
#     348.423,
#     17.969,
#     184.784,
#     304.236,
#     0
# ]

offsets = [ # This is for 2022
    45.013,
    0.113,
    46.36,
    3.577,
    90.026,
    44.031,
    348.805,
    213.77879, 
    186.65,
    45.126,
    0
]

names = [
    'M2',
    'S2',
    'N2',
    'K1',
    'M4',
    'O1',
    'P1',
    'L2',
    'K2',
    'MS4',
    'Z0'
]

harmonics = []

for i in range(len(frequencies)):
    f = frequencies[i]
    offset = offsets[i]
    harmonic = get_harmonic(f, x, d, offset)
    harmonics.append(harmonic)
    d = subtract(d, get_wave([harmonic], x, [offset]))

z0 = (0, sum(d) / len(d), 0)
harmonics.append(z0)

values = []
for i in range(len(names)):
    values.append([names[i], str(harmonics[i][1]), str((harmonics[i][2]) % 360)])

# TODO: Write to an output file that the user specifies
output = open('harmonics.csv', 'w')
output_csv = '\n'.join([','.join(h) for h in values])
print(output_csv)
output.write(output_csv)
output.close()

wave = get_wave(harmonics, x, offsets)

plt.plot(x, original)
plt.plot(x, wave)
# plt.plot(x, subtract(original, wave))
plt.show()
