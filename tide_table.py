import datetime
import matplotlib.pyplot as plt
import math

start = datetime.datetime(2022, 1, 1)

tides = [
    (True, (datetime.datetime(2022, 1, 10, 1, 42) - start).total_seconds() / 3600, 3.25),
    (False, (datetime.datetime(2022, 1, 10, 8, 23) - start).total_seconds() / 3600, 0.61),
    (True, (datetime.datetime(2022, 1, 10, 14, 0) - start).total_seconds() / 3600, 2.71),
    (False, (datetime.datetime(2022, 1, 10, 19, 27) - start).total_seconds() / 3600, 0.39),
    (True, (datetime.datetime(2022, 1, 11, 2, 37) - start).total_seconds() / 3600, 3.13),
    (False, (datetime.datetime(2022, 1, 11, 9, 25) - start).total_seconds() / 3600, 0.6),
    (True, (datetime.datetime(2022, 1, 11, 14, 56) - start).total_seconds() / 3600, 2.54),
    (False, (datetime.datetime(2022, 1, 11, 20, 20) - start).total_seconds() / 3600, 0.4),
    (True, (datetime.datetime(2022, 1, 12, 3, 37) - start).total_seconds() / 3600, 3.07),
    (False, (datetime.datetime(2022, 1, 12, 10, 10) - start).total_seconds() / 3600, 0.53),
    (True, (datetime.datetime(2022, 1, 12, 15, 56) - start).total_seconds() / 3600, 2.47),
    (False, (datetime.datetime(2022, 1, 12, 21, 11) - start).total_seconds() / 3600, 0.36),
    (True, (datetime.datetime(2022, 1, 13, 4, 34) - start).total_seconds() / 3600, 3.08),
    (False, (datetime.datetime(2022, 1, 13, 10, 50) - start).total_seconds() / 3600, 0.43),
    (True, (datetime.datetime(2022, 1, 13, 16, 52) - start).total_seconds() / 3600, 2.53),
    (False, (datetime.datetime(2022, 1, 13, 21, 59) - start).total_seconds() / 3600, 0.26),
    (True, (datetime.datetime(2022, 1, 14, 5, 24) - start).total_seconds() / 3600, 3.14),
    (False, (datetime.datetime(2022, 1, 14, 11, 27) - start).total_seconds() / 3600, 0.31),
    (True, (datetime.datetime(2022, 1, 14, 17, 40) - start).total_seconds() / 3600, 2.65),
    (False, (datetime.datetime(2022, 1, 14, 22, 45) - start).total_seconds() / 3600, 0.14),
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

wave_x = [t / 60 for t in range(int(tides[0][1] * 60), int(tides[-1][1] * 60))]
wave_y = []
wave_idx = 0
for t in wave_x:
    if t > waves[min(wave_idx, len(waves) - 1)][0]:
        wave_idx += 1
    wave = waves[min(wave_idx, len(waves) - 1)][1]
    wave_y.append(wave[1] * math.cos(wave[0] * t - wave[2]) + wave[3])


f = open('tides.csv', 'w')
f.write(','.join([str(v) for v in wave_y]))
f.close()

plt.plot(x, y)
plt.plot(wave_x, wave_y)
plt.show()