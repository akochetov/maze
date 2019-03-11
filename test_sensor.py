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
            ret[i] = round(sums[i] / amounts[i])

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
SPI = False
SPI_channels = [0, 1, 2, 3, 4, 5, 6]
k_means_clusters = [500, 900]
test_time = 10
sleep_time = 1 / 100

if SPI:
    line_sensor = SPiLineSensorSource(
        settings.LINE_SENSORS,
        Orientation.SOUTH,
        invert=True)
else:
    line_sensor = RPiLineSensorSource(
        settings.SPI_LINE_SENSOR_CHANNELS,
        Orientation.SOUTH,
        settings.SPI_LINE_SENSOR_PARAMS["MIN"],
        settings.SPI_LINE_SENSOR_PARAMS["MID"],
        settings.SPI_LINE_SENSOR_PARAMS["MAX"],
        invert=True)

print('Calibrating line sensors. Move sensor \
    line above the line to see readings:')

samples = [0] * int(test_time / sleep_time) * len(SPI_channels)
sample_clusters = [0] * int(test_time / sleep_time) * len(SPI_channels)
k = 0

for i in range(int(test_time / sleep_time)):
    if SPI:
        for i in SPI_channels:
            samples[k] = line_sensor.spi_read(i)
            k += 1

    data = line_sensor.get_state()

    print(bin(data))
    sleep(sleep_time)

print('Calibration values: {}'.format(
    k_means(samples, sample_clusters, clusters)))
print('Test finished.')

GPIO.cleanup()
