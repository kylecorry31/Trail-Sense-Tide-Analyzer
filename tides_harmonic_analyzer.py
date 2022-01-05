import matplotlib.pyplot as plt
import math

# the tide.csv file is in 1 minute increments (TODO: allow the time of each sample to be specified / the interval)
d = list(map(float, open('tide.csv', 'r').read().split(',')))
x = [i/60 for i in range(len(d))]

def get_harmonic(f, x, y):
    cos = 0
    sin = 0
    for i in range(len(x)):
        psin = y[i] * math.sin(f * x[i])
        pcos = y[i] * math.cos(f * x[i])
        cos += pcos * (x[1] - x[0])
        sin -= psin * (x[1] - x[0])
    sin /= x[-1] / 2
    cos /= x[-1] / 2

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

m2 = get_harmonic(math.radians(28.984104), x, d)
d = subtract(d, get_wave([m2], x))
s2 = get_harmonic(math.radians(30), x, d)
d = subtract(d, get_wave([s2], x))
n2 = get_harmonic(math.radians(28.43973), x, d)
d = subtract(d, get_wave([n2], x))
k1 = get_harmonic(math.radians(15.041069), x, d)
d = subtract(d, get_wave([k1], x))
m4 = get_harmonic(math.radians(57.96821), x, d)
d = subtract(d, get_wave([m4], x))
o1 = get_harmonic(math.radians(13.943035), x, d)
d = subtract(d, get_wave([o1], x))
p1 = get_harmonic(math.radians(14.958931), x, d)
d = subtract(d, get_wave([p1], x))
l2 = get_harmonic(math.radians(29.528479), x, d)
d = subtract(d, get_wave([l2], x))
k2 = get_harmonic(math.radians(30.082138), x, d)
d = subtract(d, get_wave([k2], x))
ms4 = get_harmonic(math.radians(58.984104), x, d)
d = subtract(d, get_wave([ms4], x))
z0 = (0, sum(d) / len(d), 0)

harmonics = [m2, s2, n2, k1, m4, o1, p1, l2, k2, ms4, z0]

print('\n'.join([str([math.degrees(h[0]), h[1], h[2]]) for h in harmonics]))

wave = get_wave(harmonics, x)

plt.plot(x, original)
plt.plot(x, wave)
plt.show()
