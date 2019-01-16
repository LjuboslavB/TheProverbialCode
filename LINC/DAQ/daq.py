import serial
import time
import numpy as np
import time
from threading import Thread
a = serial.Serial('COM6', 115200, timeout=2)
k = 0
c = 0
started = 0
page_points = 0
max_page_points = 10000
samples = 10000
channels = 6
data_log=np.zeros((samples, 2 + channels))
data_file = open('test_logs' + str(int(time.time())) + '.txt', 'a+')
str_data = ''
print('Starting DAQ')
a.flushOutput()
a.flushInput()
while k < samples:
    try:
        if started == 0:
            a.flushOutput()
            a.flushInput()
            started = 1
        data = a.read(a.inWaiting()).decode('UTF-8')
        if data:
            while data[-1] != '\n':
                data += a.read(a.inWaiting()).decode('UTF-8')
            str_data += data
            data = data.strip().split('\r\n')
            old_k = k
            page_points = page_points + len(data)
            k = k + len(data)
            c += 1
            try:
                data_log[old_k:k, :] = np.array([n.split(',')[:] for n in data])
            except Exception:
                print(data)
                try:
                    data_log[old_k:, :] = np.array([n.split(',')[:] for n in data])[0:samples-old_k]
                except Exception:
                    print('start shit')
            if c % 20 == 0:
                print(str(c) + ' still chugging along')
            if page_points % 100 == 0 or page_points >= max_page_points or k >= samples:
                _ = data_file.write(str_data)
                if k < samples and page_points>=max_page_points:
                    data_file.close()
                    data_file = open('test_logs' + str(int(time.time())) + '.txt', 'a+')
                page_points = 0
                str_data = ''
    except UnicodeDecodeError:
        print('no decode')

print(data_log)

