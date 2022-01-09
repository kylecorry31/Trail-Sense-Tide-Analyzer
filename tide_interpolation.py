import datetime
import matplotlib.pyplot as plt
import math

start = datetime.datetime(2021, 1, 1)

tides = [
    (False, (datetime.datetime(2021, 1, 1, 3, 59) - start).total_seconds() / 3600, -0.52),
    (True, (datetime.datetime(2021, 1, 1, 11, 8) - start).total_seconds() / 3600, 4.5),
    (False, (datetime.datetime(2021, 1, 1, 17, 18) - start).total_seconds() / 3600, -0.42),
    # (True, (datetime.datetime(2021, 1, 1, 23, 33) - start).total_seconds() / 3600, 3.63),
    # (False, (datetime.datetime(2021, 1, 2, 4, 54) - start).total_seconds() / 3600, -0.64),
    (True, (datetime.datetime(2021, 1, 2, 12, 2) - start).total_seconds() / 3600, 4.66),
    (False, (datetime.datetime(2021, 1, 2, 18, 14) - start).total_seconds() / 3600, -0.49),
    (True, (datetime.datetime(2021, 1, 3, 0, 26) - start).total_seconds() / 3600, 3.81),
]


f = 28.984104

def calculate_wave_between(p1, p2, f):
    # TODO: The amplitude does not work if p1 and p2 are the same tide type
    period = p2[1] - p1[1]
    height_delta = abs(p2[2] - p1[2])
    offset = height_delta / 2 + min(p1[2], p2[2])
    frequency = math.radians(360 / (2 * period)) * (2 if p1[0] == p2[0] else 1)
    below = frequency * (2 ** math.floor(math.log2(f / frequency)) + 1)
    above = frequency * (2 ** math.ceil(math.log2(f / frequency)) + 1)

    if abs(f - below) < abs(f - above):
        frequency = below
    else:
        frequency = above

    amplitude = (1 if p1[0] else -1) * height_delta / 2
    phase = frequency * p1[1]
    return (frequency, amplitude, phase, offset)

def get_wave_between(p1, p2):
    if (p1 == tides[2]):
        return calculate_wave_between(p1, p2, math.radians(f))
    period = p2[1] - p1[1]
    height_delta = abs(p2[2] - p1[2])
    offset = height_delta / 2 + min(p1[2], p2[2])
    frequency = math.radians(360 / (2 * period))
    amplitude = (1 if p1[0] else -1) * height_delta / 2
    phase = frequency * p1[1]
    return (frequency, amplitude, phase, offset)

print(calculate_wave_between(tides[2], tides[3], math.radians(f)))

x = [tide[1] for tide in tides]
y = [tide[2] for tide in tides]

waves = []
for i in range(1, len(tides)):
    waves.append((tides[i][1], get_wave_between(tides[i - 1], tides[i])))

wave_x = [t / 60 for t in range(int(tides[0][1] * 60), int(tides[-1][1] * 60))]
wave_y = []
wave_idx = 0
for t in wave_x:
    if t > waves[min(wave_idx, len(waves) - 1)][0]:
        wave_idx += 1
    wave = waves[min(wave_idx, len(waves) - 1)][1]
    wave_y.append(wave[1] * math.cos(wave[0] * t - wave[2]) + wave[3])

plt.plot(x, y)
plt.plot(wave_x, wave_y)
plt.show()