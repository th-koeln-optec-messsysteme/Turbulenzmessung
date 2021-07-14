import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import seaborn as sb


Counter = 0
Temperature = []
Humidity = []
Height = []
VertSpeed = []
WindSpeed = []

with open('Radiosonde_O2100002_2021-01-27-12.csv', 'r') as csv_file:
#with open('FinalCSV.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for line in csv_reader:            

        if not line[12] or not line[10] or not line[4] or not line[9] or not line[7]:
            pass
        else:
            WindSpeed.append(float(line[7]))
            VertSpeed.append(float(line[9]))
            Temperature.append(float(line[10]))
            Humidity.append(float(line[12]))
            Height.append(float(line[4]))
            Counter +=1   


    fig, (ax0, ax1, ax2, ax3) = plt.subplots(1,4, sharey=True)
    
    
    ax0.plot(Temperature, Height)
    ax0.set_ylabel('Height[m]')
    ax0.set_xlabel('Temperature[°C]')
    ax0.grid()

    ax1.plot(Humidity, Height)
    ax1.set_xlabel('Humidity[%]')
    ax1.grid()

    ax2.plot(VertSpeed, Height)
    ax2.set_xlabel('Vertical Speed[m/s]')
    ax2.grid()

    ax3.plot(WindSpeed, Height)
    ax3.set_xlabel('Wind Speed[m/s]')
    ax3.grid()
    
    plt.show()
    
    
    #data = pd.read_csv('Radiosonde_O2100002_2021-01-27-12.csv')
    data = pd.read_csv('FinalCSV.csv')
    dataplot = print(data.corr())
    sb.heatmap(data.corr(), cmap="YlGnBu", annot=True)
    plt.show()
