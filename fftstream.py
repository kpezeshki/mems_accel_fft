from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
import statistics

port = "/dev/cu.usbmodem14301"

arduino = serial.Serial(port)
sampletime = time.time()

# much cleaner to make these circular buffers
sampletimes = []
xaccels = []
yaccels = []
zaccels = []

def fft(sampletimes, xaccels, yaccels, zaccels):
    meansamplefreq = statistics.mean(sampletimes)

    # x

    xfft = fftpack.fft(xaccels)
    xfft_freqs = fftpack.fftfreq(len(xaccels))*(1/meansamplefreq)

    plt.plot(xfft_freqs, xfft)

    plt.xlim([0,100])
    plt.yscale('log')

    plt.title("x fft")
    plt.savefig("xfft")
    plt.close()

    # y

    yfft = fftpack.fft(yaccels)
    yfft_freqs = fftpack.fftfreq(len(yaccels))*(1/meansamplefreq)

    plt.plot(yfft_freqs, yfft)

    plt.xlim([0,100])
    plt.yscale('log')

    plt.title("y fft")
    plt.savefig("yfft")
    plt.close()

    # z

    zfft = fftpack.fft(zaccels)
    zfft_freqs = fftpack.fftfreq(len(zaccels))*(1/meansamplefreq)

    plt.plot(zfft_freqs, zfft)

    plt.xlim([0,100])
    plt.yscale('log')

    plt.title("z fft")
    plt.savefig("zfft")
    plt.close()





while True:
    line = arduino.readline().decode('utf-8')

    if line[0] == "|":
        sampletimes.append(time.time()-sampletime)
        accels = line.split("|")[1].split("\r\n")[0].split(",")
        xaccels.append(float(accels[0]))
        yaccels.append(float(accels[1]))
        zaccels.append(float(accels[2]))

        if len(sampletimes) == 5000:
            fft(sampletimes, xaccels, yaccels, zaccels)
            sampletimes = []
            xaccels = []
            yaccels = []
            zaccels = []

    sampletime = time.time()
    print(len(sampletimes),line)
