import datetime
import matplotlib.pyplot as plt
import math

start = datetime.datetime(2021, 1, 1)

tides = [
    (False, (datetime.datetime(2021, 1, 1, 3, 59) - start).total_seconds() / 3600, -0.52),
    (True, (datetime.datetime(2021, 1, 1, 11, 8) - start).total_seconds() / 3600, 4.5),
    (False, (datetime.datetime(2021, 1, 1, 17, 18) - start).total_seconds() / 3600, -0.42),
    (True, (datetime.datetime(2021, 1, 1, 23, 33) - start).total_seconds() / 3600, 3.63),
]


def get_wave_between(p1, p2):
    period = p2[1] - p1[1]
    height_delta = abs(p2[2] - p1[2])
    offset = height_delta / 2 + min(p1[2], p2[2])
    frequency = math.radians(360 / (2 * period))
    amplitude = (1 if p1[0] else -1) * height_delta / 2
    phase = frequency * p1[1]
    return (frequency, amplitude, phase, offset)


x = [tide[1] for tide in tides]
y = [tide[2] for tide in tides]

waves = []
for i in range(1, len(tides)):
    waves.append((tides[i][1], get_wave_between(tides[i - 1], tides[i])))

wave = get_wave_between(tides[0], tides[1])
wave_x = [t / 60 for t in range(0, 24 * 60)]

wave_y = []
wave_idx = 0
for t in wave_x:
    if t > waves[min(wave_idx, len(waves) - 1)][0]:
        wave_idx += 1
    wave = waves[min(wave_idx, len(waves) - 1)][1]
    wave_y.append(wave[1] * math.cos(wave[0] * t - wave[2]) + wave[3])

print(waves)

plt.plot(x, y)
plt.plot(wave_x, wave_y)
plt.show()