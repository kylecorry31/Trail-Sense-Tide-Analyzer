import matplotlib.pyplot as plt
import math
import datetime
import pytz

input_file = open('noaa-tides.csv', 'r')

EST = pytz.timezone('US/Eastern')
UTC = pytz.timezone('GMT')
start = datetime.datetime(2021, 1, 1, tzinfo=EST)
start_delta = 0 #(start - datetime.datetime(2021, 1, 1, tzinfo=UTC)).total_seconds() / 3600

# d = list(map(float, input_file.read().split(',')))
d = list(map(lambda line: float(line.split(',')[1]), input_file.readlines()[1:]))
input_file.close()

# TODO Use the times in the CSV file
# TODO Convert the phases to be relative to Jan 1 of the year in UTC

x = [i/10 + start_delta for i in range(len(d))]
# d = [math.cos(5 * i) + 0.5 * math.cos(12 * i) for i in x]

def get_harmonic(f, x, y):
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

    phase = math.degrees(math.atan2(sin, cos))
    amplitude = math.hypot(sin, cos)

    return (f, amplitude, phase)


def get_wave(harmonics, x):
    wave = []
    for i in range(len(x)):
        total = 0
        for h in harmonics:
            total += h[1] * math.cos(h[0] * x[i] + math.radians(h[2]))
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

for f in frequencies:
    harmonic = get_harmonic(f, x, d)
    harmonics.append(harmonic)
    d = subtract(d, get_wave([harmonic], x))

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

wave = get_wave(harmonics, x)

plt.plot(x, original)
plt.plot(x, wave)
# plt.plot(x, subtract(original, wave))
plt.show()
