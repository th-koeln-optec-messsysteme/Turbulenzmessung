import csv

in_file_1 = open('RS41 Tracker Export 2021-01-27 D01.csv.csv', 'r')
in_file_2 = open('Final CSV Two combined von Johannes.csv', 'r')

in_file_1_reader = csv.reader(in_file_1)
in_file_2_reader = csv.reader(in_file_2)

with open('FinalCSV.csv', 'w') as out_file:
    out_file_reader = csv.reader(out_file)
    out_file.writelines('Date,Time,Latitude,Longitude,Altitude,Battery Voltage (V),Sats used,Wind Speed (m/s),Wind Dir (deg),Vertical Speed (m/s),Temperature(deg),Pressure (hPa),Humidity (%),Dew point (deg),variance_accX, variance_accY, variance_accZ, variance_gyrX, variance_gyrY, variance_gyrZ  \n')

    #Compare two CSV filed to find matching values

    masterlist = list(in_file_2_reader)
    
    for hosts_row in in_file_1_reader:
        row = 1
        found = False
        for master_row in masterlist:
            results_row = hosts_row
            if hosts_row[1] == master_row[1]:
                #out_file.writelines(hosts_row + ',' + master_row[3]+ ',' + master_row[4]+ ',' + master_row[5]+ ',' + master_row[6]+ ',' + master_row[7]+ ',' + master_row[8] + '\n')
                out_file.writelines(str(hosts_row[0]) + ',' + str(hosts_row[1]) + ',' +str(hosts_row[2]) + ',' +str(hosts_row[3]) + ',' +str(hosts_row[4]) + ',' +str(hosts_row[5]) + ',' +str(hosts_row[6]) + ',' +str(hosts_row[7]) + ',' +str(hosts_row[8]) + ',' +str(hosts_row[9]) + ',' +str(hosts_row[10]) + ',' +str(hosts_row[11]) + ',' +str(hosts_row[12]) + ',' +str(hosts_row[13]) + ',' + str(master_row[3])+ ',' + str(master_row[4])+ ',' + str(master_row[5])+ ',' + str(master_row[6])+ ',' + str(master_row[7])+ ',' + str(master_row[8]) + '\n')
                #print(hosts_row + master_row)
                print(str(hosts_row[0]) + ',' + str(hosts_row[1]) + ',' +str(hosts_row[2]) + ',' +str(hosts_row[3]) + ',' +str(hosts_row[4]) + ',' +str(hosts_row[5]) + ',' +str(hosts_row[6]) + ',' +str(hosts_row[7]) + ',' +str(hosts_row[8]) + ',' +str(hosts_row[9]) + ',' +str(hosts_row[10]) + ',' +str(hosts_row[11]) + ',' +str(hosts_row[12]) + ',' +str(hosts_row[13]) + ',' + str(master_row[3])+ ',' + str(master_row[4])+ ',' + str(master_row[5])+ ',' + str(master_row[6])+ ',' + str(master_row[7])+ ',' + str(master_row[8]) + '\n')
                found = True
                break
            row = row + 1
        if not found:
            results_row.append('NOT FOUND in master list')

    

in_file_1.close()
in_file_2.close()
out_file.close()
