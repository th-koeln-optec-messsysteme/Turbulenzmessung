import csv
import os
import operator
import statistics

WRITTEN = 0

fileone = open('XDATA 2021-01-27 D01+Variance.csv', 'r')
filetwo = open('XDATA 2021-01-27 D02+Variance.csv', 'r')
next(filetwo) #(Date, Time, ...) vom 2.

fileone_reader = fileone.readlines() #Erste
filetwo_reader = filetwo.readlines() #Zweite


#Combiner
with open('TempFirstWriter.csv', 'w') as outFile:
    for line in fileone_reader:
        outFile.write(line)
        #print("printing1")

    for line in filetwo_reader:
        outFile.write(line)
        #print("printing2")
        
outFile.close()

#DopplerLöscher
with open('TempFirstWriter.csv','r') as in_file, open('TempDoppelteGelöscht.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)
        #print("printing3")

out_file.close        


#DatumSortieren
sample = open('TempDoppelteGelöscht.csv', 'r')
next(sample)
csv1 = csv.reader(sample, delimiter=',')
sort = sorted(csv1,key=operator.itemgetter(1))

with open('XDATA 2021-01-27 D01+D02 + Variance.csv', 'w') as writer:
    writer.writelines("(0)Date, (1)Time, (2)Framenumber, (3)accX1, (4)accY1, (5)accZ1, (6)gyrX1, (7)gyrY1, (8)gyrZ1, (9)accX2, (10)accY2, (11)accZ2, (12)gyrX2, (13)gyrY2, (14)gyrZ2, (15)accX3, (16)accY3, (17)accZ3, (18)gyrX3, (19)gyrY3, (20)gyrZ3, (21)accX4, (22)accY4, (23)accZ4, (24)gyrX4, (25)gyrY4, (26)gyrZ4, (27)accX5, (28)accY5, (29)accZ5, (30)gyrX5, (31)gyrY5, (32)gyrZ5 , (33)variance_accX, (34)variance_accY, (35)variance_accZ, (36)variance_gyrX, (37)variance_gyrY, (38)variance_gyrZ \n")
    for line in sort:
        for n in range (39):
            writer.writelines(line[n])
            writer.writelines(',')
        writer.writelines('\n')
        WRITTEN+=1
        
print("Es Wurden " + str(WRITTEN) + " Datensätze in 'XDATA 2021-01-27 D01+D02 + Variance.csv' geschrieben")
    
sample.close()
writer.close()


#os.unlink('ReadyToCombineZweite.csv') #Löschen der Statistik datei
os.unlink('TempDoppelteGelöscht.csv') #Löschen der Doppler löscher Datei
os.unlink('TempFirstWriter.csv') #Löschen der Combiner Datei

os.system("pause") 
