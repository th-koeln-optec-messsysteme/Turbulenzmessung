import csv
import os
import operator
import statistics

WRITTEN = 0

sample = open('XDATA + RS41_Tracker.csv', 'r')
next(sample)
csv1 = csv.reader(sample, delimiter=',')

with open('RS41_Tracker + Gyro-Time-Subframed.csv', 'w') as writer:
    
    writer.writelines("[0]Date,[1]Time,[2]Latitude,[3]Longitude,[4]Altitude,[5]Battery Voltage (V),[6]Sats used,[7]Wind Speed (m/s),[8]Wind Dir (deg),[9]Vertical Speed (m/s),[10]Temperature(deg),[11]Pressure (hPa),[12]Humidity (%),[13]Dew point (deg), [14]accX, [15]accY, [16]accZ, [17]gyrX, [18]gyrY, [19]gyrZ, [20]variance_accX, [21]variance_accY, [22]variance_accZ, [23]variance_gyrX,[24]variance_gyrY,[25]variance_gyrZ \n")

    for line in csv1:
        writer.writelines(line[0]+','+line[1]+':00,')
        for i in range(2,14):
            writer.writelines(line[i]+',')
        for n in range(14,20): 
            writer.writelines(line[n])
            writer.writelines(',')
        for j in range(44,50):
            writer.writelines(line[j]+',')
        writer.writelines('\n')

        writer.writelines(line[0]+','+line[1]+':20,')
        for i in range(2,14):
            writer.writelines(line[i]+',')
        for n in range(20,26):
            writer.writelines(line[n])
            writer.writelines(',')
        for j in range(44,50):
            writer.writelines(line[j]+',')
        writer.writelines('\n')

        writer.writelines(line[0]+','+line[1]+':40,')
        for i in range(2,14):
            writer.writelines(line[i]+',')
        for n in range(26,32):
            writer.writelines(line[n])
            writer.writelines(',')
        for j in range(44,50):
            writer.writelines(line[j]+',')
        writer.writelines('\n')

        writer.writelines(line[0]+','+line[1]+':60,')
        for i in range(2,14):
            writer.writelines(line[i]+',')
        for n in range(32,38):
            writer.writelines(line[n])
            writer.writelines(',')
        for j in range(44,50):
            writer.writelines(line[j]+',')
        writer.writelines('\n')


        writer.writelines(line[0]+','+line[1]+':80,')
        for i in range(2,14):
            writer.writelines(line[i]+',')
        for n in range(38,44):
            writer.writelines(line[n])
            writer.writelines(',')
        for j in range(44,50):
            writer.writelines(line[j]+',')
        writer.writelines('\n')

        WRITTEN+=5

print("Es wurden " +str(WRITTEN) + " Datensätze in 'RS41_Tracker + Gyro-Time-Subframed.csv' geschrieben.") 

sample.close()
writer.close()

os.system("pause")
