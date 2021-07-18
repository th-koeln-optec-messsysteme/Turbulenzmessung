import csv
import os

WRITTEN = 0

in_file_1 = open('RS41 Tracker Export 2021-01-27 D01.csv', 'r')
in_file_2 = open('XDATA 2021-01-27 D01+D02 + Variance.csv', 'r')

in_file_1_reader = csv.reader(in_file_1)
in_file_2_reader = csv.reader(in_file_2)

with open('XDATA + RS41_Tracker.csv', 'w') as out_file:
    out_file_reader = csv.reader(out_file)
    out_file.writelines('[0]Date,[1]Time,[2]Latitude,[3]Longitude,[4]Altitude,[5]Battery Voltage (V),[6]Sats used,[7]Wind Speed (m/s),[8]Wind Dir (deg),[9]Vertical Speed (m/s),[10]Temperature(deg),[11]Pressure (hPa),[12]Humidity (%),[13]Dew point (deg),[14]accX1,[15]accY1,[16]accZ1,[17]gyrX1,[18]gyrY1,[19]gyrZ1,[20]accX2,[21]accY2,[22]accZ2,[23]gyrX2,[24]gyrY2,[25]gyrZ2,[26]accX3,[27]accY3,[28]accZ3, [29]gyrX3,[30]gyrY3, [31]gyrZ3, [32]accX4, [33]accY4, [34]accZ4, [35]gyrX4, [36]gyrY4,  [37]gyrZ4, [38]accX5, [39]accY5, [40]accZ5, [41]gyrX5, [42]gyrY5, [43]gyrZ5 , [44]variance_accX, [45]variance_accY,  [46]variance_accZ, [47]variance_gyrX, [48]variance_gyrY, [49]variance_gyrZ   \n')
    #Compare two CSV filed to find matching values

    masterlist = list(in_file_2_reader)
    
    for hosts_row in in_file_1_reader:
        row = 1
        found = False
        for master_row in masterlist:
            results_row = hosts_row
            if hosts_row[1] == master_row[1]:
                WRITTEN +=1
                

                for n in range(14):
                    out_file.writelines(str(hosts_row[n]) + ',')
                for n in range(3,39):
                    out_file.writelines(str(master_row[n]) + ',')
                out_file.writelines('\n')
                found = True
                break
            row = row + 1
        if not found:
            results_row.append('NOT FOUND in master list')

print("Es wurden " +str(WRITTEN)+ " Datensätze in 'XDATA + RS41_Tracker.csv' geschrieben." )    

in_file_1.close()
in_file_2.close()
out_file.close()

os.system("pause")
