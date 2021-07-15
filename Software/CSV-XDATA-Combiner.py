import csv
import os
import operator
import statistics

fileone = open('XDATA 2021-01-27 D01', 'r')
filetwo = open('XDATA 2021-01-27 D02', 'r')
next(filetwo) #(Date, Time, ...) vom 2.

fileone_reader = fileone.readlines() #Erste
filetwo_reader = filetwo.readlines() #Zweite


#Combiner
with open('TempFirstWriter.csv', 'w') as outFile:
    for line in fileone_reader:
        outFile.write(line)
        print("printing1")

    for line in filetwo_reader:
        outFile.write(line)
        print("printing2")
        
outFile.close()

#Statistics Script
geloescht = 0

mid_accX = 0
mid_accY = 0
mid_accZ = 0

mid_gyrX = 0
mid_gyrY = 0
mid_gyrZ = 0

in_file = open('TempFirstWriter.csv', 'r')
out_file = open('ReadyToCombineZweite.csv', 'w')
next(in_file)

out_file.writelines("Date, Time, Frame, variance_accX, variance_accY, variance_gyrX, variance_gyrY, variance_gyrZ, \n")

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

            
            out_file.writelines(frame[0] + ',' + frame[1] +','+ frame[2] +','+ str(TESTEM1) +','+ str(TESTEM2) +','+ str(TESTEM3) +','+ str(TESTEM4) +','+ str(TESTEM5) +','+ str(TESTEM6) + '\n')

            print("printing")
out_file.close()
in_file.close()


#DopplerLöscher
with open('ReadyToCombineZweite.csv','r') as in_file, open('TempDoppelteGelöscht.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)
        print("printing3")

out_file.close        


#DatumSortieren
sample = open('TempDoppelteGelöscht.csv', 'r')
next(sample)
csv1 = csv.reader(sample, delimiter=',')
sort = sorted(csv1,key=operator.itemgetter(1))

with open('TempNachZeitSortiert.csv', 'w') as writer:
    writer.writelines("Date, Time, Frame, variance_accX, variance_accY, variance_accZ, variance_gyrX, variance_gyrY, variance_gyrZ \n")
    for line in sort:
        writer.writelines(line[0] + ',' +line[1] + ',' +line[2] + ',' +line[3] + ',' +line[4] + ',' +line[5] + ',' + line[6] +',' + line[7] +',' + line[8])
        writer.writelines('\n')
        print('printing4')
    
sample.close()
writer.close()
os.unlink('ReadyToCombineZweite.csv') #Löschen der Statistik datei
os.unlink('TempDoppelteGelöscht.csv') #Löschen der Doppler löscher Datei
os.unlink('TempFirstWriter.csv') #Löschen der Combiner Datei
