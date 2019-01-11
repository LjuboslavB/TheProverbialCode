import serial
import time
import numpy as np
from threading import Thread
a = serial.Serial('COM6', 115200, timeout=2)
a.flushInput()
a.flushOutput()
k = -1
samples = 1000
channels = 6
data_log=np.zeros((samples, 2 + channels))
data_file = open('test_logs.txt', 'a+')
time.sleep(0.001)
str_data = ''
while k < samples-1:
    try:
        data = a.read(a.inWaiting()).decode('UTF-8')
        if data:
            while data[-1] != '\n':
                data += a.read(a.inWaiting()).decode('UTF-8')
            k = k + 1
            str_data += data
            data = data.strip().split('\r\n')
            data_log[k, :] = data[0].split(',')
            if k % 100 == 0:
                print(str(k) + ' still chugging along')
    except a.SerialTimeoutException:
        print('Could not read')
    if k % 10 == 0 or k == samples-1:
        _ = data_file.write(str_data)
        str_data = ''

data_file.close()
print(data_log)
