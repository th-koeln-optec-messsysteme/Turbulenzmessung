import csv
import numpy as np
import matplotlib.pyplot as plt

Time_Counter = 1
Time = []
Temperature = []
Humidity = []
Height = []

with open('Radiosonde_O2100002_2021-01-27-12.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for line in csv_reader:
        
        Time.append(Time_Counter)
        Temperature.append(line[10])
        Humidity.append(line[12])
        Height.append(line[4])
        Time_Counter +=1
        
        if Time_Counter == 1000:    #break nach den ersten 1000 sec (erstmal)
            break
        
        
    fig, axs = plt.subplots(3)
    axs[0].plot(Time, Temperature)
    axs[0].set_ylabel('Temperature')
    axs[0].set_yticks([0, 15, 25, 35, 45, 52])
    
    axs[1].plot(Time, Humidity)
    axs[1].set_ylabel('Humidity')
    axs[1].set_yticks([0, 50, 100, 150, 190])
    
    axs[2].plot(Time, Height)
    axs[2].set_ylabel('Height')
    axs[2].set_yticks([0, 100,200,300,400,500])


    plt.show()
