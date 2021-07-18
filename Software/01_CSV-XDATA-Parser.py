import struct
import csv
import os
import operator
import statistics

CounterDEL = 0
CounterWRIT = 0

in_file_name = 'Raw 2021-01-27 D01.txt'
out_file_name = 'XDATA 2021-01-27 D01.csv'
line_ending = '\n'

CRC16_INITIAL_VALUE = 0xFFFF
CRC16_XOR_OUT = 0x0000
CRC16_POLYNOMIAL = 0x1021

def crc16(data):
    xor_in = CRC16_INITIAL_VALUE  # initial value
    xor_out = CRC16_XOR_OUT  # final XOR value
    poly = CRC16_POLYNOMIAL  # generator polinom (normal form)

    reg = xor_in
    for octet in data:
        # reflect in
        for i in range(8):
            topbit = reg & 0x8000
            if octet & (0x80 >> i):
                topbit ^= 0x8000
            reg <<= 1
            if topbit:
                reg ^= poly
        reg &= 0xFFFF
        # reflect out
    return reg ^ xor_out

def gps_timestamp_to_time_string(gpsweek, gpsseconds, leapseconds):
    import datetime
    datetimeformat = "%Y-%m-%d,%H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06,00:00:00", datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek * 7), seconds=(gpsseconds - leapseconds))
    return datetime.datetime.strftime(epoch + elapsed, datetimeformat)


if __name__ == '__main__':
    zeros = bytes.fromhex('16 01 4F 50 54 45 43 30 30 31 16 00 00 00 00 00 1D 40 00 00 00 00 32 16 CD CC CC 3D BD FF 4B BF 47 49 9E BD 66 36 B1 33'.strip())
    #print(zeros)
    #print(hex(crc16(zeros)))

    in_file = open(in_file_name, 'r')
    out_file = open(out_file_name, 'w')
    frames = in_file.readlines()

    out_file.writelines("(0)Date, (1)Time, (2)Framenumber, (3)accX1, (4)accY1, (5)accZ1, (6)gyrX1, (7)gyrY1, (8)gyrZ1, (9)accX2, (10)accY2, (11)accZ2, (12)gyrX2, (13)gyrY2, (14)gyrZ2, (15)accX3, (16)accY3, (17)accZ3, (18)gyrX3, (19)gyrY3, (20)gyrZ3, (21)accX4, (22)accY4, (23)accZ4, (24)gyrX4, (25)gyrY4, (26)gyrZ4, (27)accX5, (28)accY5, (29)accZ5, (30)gyrX5, (31)gyrY5, (32)gyrZ5" + line_ending)

    for frame in frames:
        raw_string = frame.strip()      #Jeweils die Kopie einer Zeile
        frame_bytes = bytes.fromhex(raw_string)

        frame_number = (frame_bytes[0x3c] << 8) | frame_bytes[0x3b]
        gps_week = (frame_bytes[0x96] << 8) | frame_bytes[0x95]
        gps_time_of_week = (frame_bytes[0x9A] << 24) | (frame_bytes[0x99] << 16) | (frame_bytes[0x98] << 8) | frame_bytes[0x97]

        xdata_length = frame_bytes[0x12C]
        xdata_payload = frame_bytes[0x12D:(0x12D + xdata_length)]
        

        if xdata_length != 140:
            CounterDEL+=1
        #    print("errorEINS")
            continue 

        if xdata_length > len(xdata_payload):
            CounterDEL+=1
        #    print("error")
            continue

        xdata_crc = (frame_bytes[0x12D + xdata_length + 1] << 8) | frame_bytes[0x12D + xdata_length]  
        calculated_crc = crc16(xdata_payload)

        if calculated_crc != xdata_crc:
            CounterDEL+=1
        #    print("error")
            continue

        measurement_bytes = xdata_payload[20:]
        #print(len(measurement_bytes))

        if len(measurement_bytes) != 120:
            CounterDEL+=1
        #    print("hallo")
            continue
        
        formatter = '<' + 'f' * (len(measurement_bytes) // struct.calcsize('f'))
        numbers = struct.unpack(formatter, measurement_bytes)
        #print(numbers)


        keys = ['accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ']
        imu_values = [dict(zip(keys , numbers[i:i+6])) for i in range(0, 30, 6)]     #zip(keys, numbers[i:i+6]))
        #print(imu_values)



        gps_string = gps_timestamp_to_time_string(gps_week, gps_time_of_week/1000, 0)

        #print('Frame #:', frame_number,
        #      'Week:', gps_week,
        #      'TOW:', gps_time_of_week,
        #      'GPS Time:', gps_string,
        #      'xdata:', hex(xdata_length) , hex(xdata_crc)) #xdata_payload[20:].decode('utf_8', errors='ignore')


        ToSave_Numbers = str(numbers)
        ToSave_Numbers = ToSave_Numbers.replace('(','')
        ToSave_Numbers = ToSave_Numbers.replace(')','')

        #print(ToSave_Numbers)
        
        out_file.writelines(str(gps_string) + ',' + str(frame_number) + ',' + ToSave_Numbers + line_ending)
    out_file.close()


#Statistics Script
geloescht = 0

mid_accX = 0
mid_accY = 0
mid_accZ = 0

mid_gyrX = 0
mid_gyrY = 0
mid_gyrZ = 0

in_file = open('XDATA 2021-01-27 D01.csv', 'r')
out_file = open('XDATA 2021-01-27 D01+Variance.csv', 'w')

next(in_file)

out_file.writelines("(0)Date, (1)Time, (2)Framenumber, (3)accX1, (4)accY1, (5)accZ1, (6)gyrX1, (7)gyrY1, (8)gyrZ1, (9)accX2, (10)accY2, (11)accZ2, (12)gyrX2, (13)gyrY2, (14)gyrZ2, (15)accX3, (16)accY3, (17)accZ3, (18)gyrX3, (19)gyrY3, (20)gyrZ3, (21)accX4, (22)accY4, (23)accZ4, (24)gyrX4, (25)gyrY4, (26)gyrZ4, (27)accX5, (28)accY5, (29)accZ5, (30)gyrX5, (31)gyrY5, (32)gyrZ5 , (33)variance_accX, (34)variance_accY, (35)variance_accZ, (36)variance_gyrX, (37)variance_gyrY, (38)variance_gyrZ, \n")

frames = csv.reader(in_file, delimiter= ",")

for frame in frames:
      
      if str(frame[0]) == '1980-01-06' or str(frame[0]) == '1980-01-09':
            geloescht += 1
            pass
      
      else:
            j = 3
            i=0
            while i < 24:
                  mid_accX += (float(frame[j+i]))
                  i+= 6
            TESTEM1 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])])             

            j = 4                   
            i=0
            while i < 24:
                  mid_accY += (float(frame[j+i]))
                  i+= 6
            TESTEM2 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])])  

            j = 5
            i=0
            while i < 24:
                  mid_accZ += (float(frame[j+i]))
                  i+= 6
            TESTEM3 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])]) 

            j = 6
            i=0
            while i < 24:
                  mid_gyrX += (float(frame[j+i]))
                  i+= 6
            TESTEM4 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])]) 

            j = 7
            i=0
            while i < 24:
                  mid_gyrY += (float(frame[j+i]))
                  i+= 6
            TESTEM5 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])]) 

            j = 8
            i=0
            while i < 24:
                  mid_gyrZ += (float(frame[j+i]))
                  i+= 6
            TESTEM6 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])])  

            for n in range (33):
                out_file.writelines(frame[n])
                out_file.writelines(',')

            CounterWRIT +=1
            out_file.writelines(str(TESTEM1) +','+ str(TESTEM2) +','+ str(TESTEM3) +','+ str(TESTEM4) +','+ str(TESTEM5) +','+ str(TESTEM6) + '\n')

            #print("printing")
out_file.close()
in_file.close()

print("Es wurden " + str(CounterDEL+geloescht) + " Frames aus D01 verworfen")
print("Es wurden "  + str(CounterWRIT) + " Frames in D01+Variance geschrieben")












in_file_name = 'Raw 2021-01-27 D02.txt'
out_file_name = 'XDATA 2021-01-27 D02.csv'
line_ending = '\n'

CounterDEL = 0
CounterWRIT = 0

CRC16_INITIAL_VALUE = 0xFFFF
CRC16_XOR_OUT = 0x0000
CRC16_POLYNOMIAL = 0x1021

def crc16(data):
    xor_in = CRC16_INITIAL_VALUE  # initial value
    xor_out = CRC16_XOR_OUT  # final XOR value
    poly = CRC16_POLYNOMIAL  # generator polinom (normal form)

    reg = xor_in
    for octet in data:
        # reflect in
        for i in range(8):
            topbit = reg & 0x8000
            if octet & (0x80 >> i):
                topbit ^= 0x8000
            reg <<= 1
            if topbit:
                reg ^= poly
        reg &= 0xFFFF
        # reflect out
    return reg ^ xor_out

def gps_timestamp_to_time_string(gpsweek, gpsseconds, leapseconds):
    import datetime
    datetimeformat = "%Y-%m-%d,%H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06,00:00:00", datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek * 7), seconds=(gpsseconds - leapseconds))
    return datetime.datetime.strftime(epoch + elapsed, datetimeformat)


if __name__ == '__main__':
    zeros = bytes.fromhex('16 01 4F 50 54 45 43 30 30 31 16 00 00 00 00 00 1D 40 00 00 00 00 32 16 CD CC CC 3D BD FF 4B BF 47 49 9E BD 66 36 B1 33'.strip())
    #print(zeros)
    #print(hex(crc16(zeros)))

    in_file = open(in_file_name, 'r')
    out_file = open(out_file_name, 'w')
    frames = in_file.readlines()

    out_file.writelines("(0)Date, (1)Time, (2)Framenumber, (3)accX1, (4)accY1, (5)accZ1, (6)gyrX1, (7)gyrY1, (8)gyrZ1, (9)accX2, (10)accY2, (11)accZ2, (12)gyrX2, (13)gyrY2, (14)gyrZ2, (15)accX3, (16)accY3, (17)accZ3, (18)gyrX3, (19)gyrY3, (20)gyrZ3, (21)accX4, (22)accY4, (23)accZ4, (24)gyrX4, (25)gyrY4, (26)gyrZ4, (27)accX5, (28)accY5, (29)accZ5, (30)gyrX5, (31)gyrY5, (32)gyrZ5" + line_ending)

    for frame in frames:
        raw_string = frame.strip()      #Jeweils die Kopie einer Zeile
        frame_bytes = bytes.fromhex(raw_string)

        frame_number = (frame_bytes[0x3c] << 8) | frame_bytes[0x3b]
        gps_week = (frame_bytes[0x96] << 8) | frame_bytes[0x95]
        gps_time_of_week = (frame_bytes[0x9A] << 24) | (frame_bytes[0x99] << 16) | (frame_bytes[0x98] << 8) | frame_bytes[0x97]

        xdata_length = frame_bytes[0x12C]
        xdata_payload = frame_bytes[0x12D:(0x12D + xdata_length)]
        

        if xdata_length != 140:
            CounterDEL+=1
        #    print("errorEINS")
            continue 

        if xdata_length > len(xdata_payload):
            CounterDEL+=1
        #    print("error")
            continue

        xdata_crc = (frame_bytes[0x12D + xdata_length + 1] << 8) | frame_bytes[0x12D + xdata_length]  
        calculated_crc = crc16(xdata_payload)

        if calculated_crc != xdata_crc:
            CounterDEL+=1
        #    print("error")
            continue

        measurement_bytes = xdata_payload[20:]
        #print(len(measurement_bytes))

        if len(measurement_bytes) != 120:
            CounterDEL+=1
        #    print("hallo")
            continue
        
        formatter = '<' + 'f' * (len(measurement_bytes) // struct.calcsize('f'))
        numbers = struct.unpack(formatter, measurement_bytes)
        #print(numbers)


        keys = ['accX', 'accY', 'accZ', 'gyrX', 'gyrY', 'gyrZ']
        imu_values = [dict(zip(keys , numbers[i:i+6])) for i in range(0, 30, 6)]     #zip(keys, numbers[i:i+6]))
        #print(imu_values)



        gps_string = gps_timestamp_to_time_string(gps_week, gps_time_of_week/1000, 0)

        #print('Frame #:', frame_number,
        #      'Week:', gps_week,
        #      'TOW:', gps_time_of_week,
        #      'GPS Time:', gps_string,
        #      'xdata:', hex(xdata_length) , hex(xdata_crc)) #xdata_payload[20:].decode('utf_8', errors='ignore')


        ToSave_Numbers = str(numbers)
        ToSave_Numbers = ToSave_Numbers.replace('(','')
        ToSave_Numbers = ToSave_Numbers.replace(')','')

        #print(ToSave_Numbers)

        out_file.writelines(str(gps_string) + ',' + str(frame_number) + ',' + ToSave_Numbers + line_ending)
    out_file.close()


#Statistics Script
geloescht = 0

mid_accX = 0
mid_accY = 0
mid_accZ = 0

mid_gyrX = 0
mid_gyrY = 0
mid_gyrZ = 0

in_file = open('XDATA 2021-01-27 D02.csv', 'r')
out_file = open('XDATA 2021-01-27 D02+Variance.csv', 'w')

next(in_file)

out_file.writelines("(0)Date, (1)Time, (2)Framenumber, (3)accX1, (4)accY1, (5)accZ1, (6)gyrX1, (7)gyrY1, (8)gyrZ1, (9)accX2, (10)accY2, (11)accZ2, (12)gyrX2, (13)gyrY2, (14)gyrZ2, (15)accX3, (16)accY3, (17)accZ3, (18)gyrX3, (19)gyrY3, (20)gyrZ3, (21)accX4, (22)accY4, (23)accZ4, (24)gyrX4, (25)gyrY4, (26)gyrZ4, (27)accX5, (28)accY5, (29)accZ5, (30)gyrX5, (31)gyrY5, (32)gyrZ5 , (33)variance_accX, (34)variance_accY, (35)variance_accZ, (36)variance_gyrX, (37)variance_gyrY, (38)variance_gyrZ, \n")

frames = csv.reader(in_file, delimiter= ",")

for frame in frames:
      
      if str(frame[0]) == '1980-01-06' or str(frame[0]) == '1980-01-09':
            geloescht += 1
            pass
      
      else:
            j = 3
            i=0
            while i < 24:
                  mid_accX += (float(frame[j+i]))
                  i+= 6
            TESTEM1 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])])             

            j = 4                   
            i=0
            while i < 24:
                  mid_accY += (float(frame[j+i]))
                  i+= 6
            TESTEM2 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])])  

            j = 5
            i=0
            while i < 24:
                  mid_accZ += (float(frame[j+i]))
                  i+= 6
            TESTEM3 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])]) 

            j = 6
            i=0
            while i < 24:
                  mid_gyrX += (float(frame[j+i]))
                  i+= 6
            TESTEM4 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])]) 

            j = 7
            i=0
            while i < 24:
                  mid_gyrY += (float(frame[j+i]))
                  i+= 6
            TESTEM5 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])]) 

            j = 8
            i=0
            while i < 24:
                  mid_gyrZ += (float(frame[j+i]))
                  i+= 6
            TESTEM6 = statistics.pstdev([float(frame[j+0]), float(frame[j+6]), float(frame[j+12]), float(frame[j+18]), float(frame[j+24])])  

            for n in range (33):
                out_file.writelines(frame[n])
                out_file.writelines(',')
                
            CounterWRIT +=1
            out_file.writelines(str(TESTEM1) +','+ str(TESTEM2) +','+ str(TESTEM3) +','+ str(TESTEM4) +','+ str(TESTEM5) +','+ str(TESTEM6) + '\n')

            #print("printing")
out_file.close()
in_file.close()

print("Es wurden " + str(CounterDEL+geloescht) + " Frames aus D02 verworfen")
print("Es wurden "  + str(CounterWRIT) + " Frames in D02+Variance geschrieben")


os.unlink('XDATA 2021-01-27 D01.csv') #Löschen
os.unlink('XDATA 2021-01-27 D02.csv') #Löschen

os.system("pause")


        
        
