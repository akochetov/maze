import RPi.GPIO as GPIO
from sensors.rpi_line_sensor_source import RPiLineSensorSource
from sensors.spi_line_sensor_source import SPiLineSensorSource
from misc.orientation import Orientation
import misc.settings as settings
from time import sleep


def k_means(samples, sample_clusters, clusters):
    def update_clusters(samples, sample_clusters):
        ret = [0] * len(clusters)
        sums = [0] * len(clusters)
        amounts = [0] * len(clusters)

        for s in range(len(samples)):
            sample = samples[s]
            sums[sample_clusters[s]] += sample
            amounts[sample_clusters[s]] += 1

        for i in range(0, len(clusters)):
            ret[i] = round(sums[i] / amounts[i]) if amounts[i] != 0 else 0

        return ret

    while True:
        for s in range(len(samples)):
            # put it in cluster indexed 0 at first
            cluster = sample_clusters[s]
            sample = samples[s]
            distance = abs(sample - clusters[cluster])
            for i in range(len(clusters)):
                if abs(sample - clusters[i]) < distance:
                    distance = abs(sample - clusters[i])
                    cluster = i
            # update cluster index for specific sample
            sample_clusters[s] = cluster

        prev_clusters = clusters
        clusters = update_clusters(samples, sample_clusters)
        if set(clusters) == set(prev_clusters):
            return clusters

GPIO.setmode(GPIO.BCM)

line_sensor = None
SPI = True
test_time = 1
sleep_time = 1 / 100

if not SPI:
    line_sensor = RPiLineSensorSource(
        settings.LINE_SENSORS,
        Orientation.SOUTH,
        invert=True)
else:
    line_sensor = SPiLineSensorSource(
        settings.SPI_LINE_SENSOR_CHANNELS,
        Orientation.SOUTH,
        settings.SPI_LINE_SENSOR_MIN_MAX,
        invert=True)

print('Calibrating line sensors. Move sensor \
    line above the line to see readings:')

samples = (
    [0] *
    int(test_time / sleep_time) *
    len(settings.SPI_LINE_SENSOR_CHANNELS)
    )

sample_clusters = (
    [0] *
    int(test_time / sleep_time) *
    len(settings.SPI_LINE_SENSOR_CHANNELS)
    )

k = 0
min = 1023
max = 0
for i in range(int(test_time / sleep_time)):
    if SPI:
        for i in settings.SPI_LINE_SENSOR_CHANNELS:
            samples[k] = line_sensor.spi_read(i)
            if samples[k] < min:
                min = samples[k]
            if samples[k] > max:
                max = samples[k]
            print(samples[k])
            k += 1

    data = line_sensor.get_state()

    print('{}\t{}'.format(bin(data), line_sensor.get_value(data)))
    sleep(sleep_time)

print('Calibration values: {}'.format(
    k_means(samples, sample_clusters, [min, max])))
print('Test finished.')

GPIO.cleanup()
