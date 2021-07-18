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


acc_x = []
acc_y = []
acc_z = []
gyr_x = []
gyr_y = []
gyr_z = []




with open('RS41 Tracker Export 2021-01-27 D01.csv', 'r') as csv_file:
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
    
    
    data = pd.read_csv('RS41_Tracker + Gyro-Time-Subframed.csv')
    dataplot = print(data.corr())
    sb.heatmap(data.corr(), cmap="YlGnBu", annot=True)
    plt.show()


with open('XDATA + RS41_Tracker.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    Temperature.clear()
    Humidity.clear()
    Height.clear()
    VertSpeed.clear()
    WindSpeed.clear()

    for line in csv_reader:            

        if not line[12] or not line[10] or not line[4] or not line[9] or not line[7]:
            pass
        else:
            WindSpeed.append(float(line[7]))
            VertSpeed.append(float(line[9]))
            Temperature.append(float(line[10]))
            Humidity.append(float(line[12]))
            Height.append(float(line[4]))

            acc_x.append(float(line[14]))
            acc_y.append(float(line[15]))
            acc_z.append(float(line[16]))
            gyr_x.append(float(line[17]))
            gyr_y.append(float(line[18]))
            gyr_z.append(float(line[19]))
            Counter +=1   


    fig, (ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9) = plt.subplots(1,10, sharey=True)
    
    
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

    ax4.plot(acc_x, Height)
    ax4.set_xlabel('acc_x')
    ax4.grid()

    ax5.plot(acc_y, Height)
    ax5.set_xlabel('acc_y')
    ax5.grid()

    ax6.plot(acc_z, Height)
    ax6.set_xlabel('acc_z')
    ax6.grid()

    ax7.plot(gyr_x, Height)
    ax7.set_xlabel('gyr_x')
    ax7.grid()

    ax8.plot(gyr_y, Height)
    ax8.set_xlabel('gyr_y')
    ax8.grid()

    ax9.plot(gyr_z, Height)
    ax9.set_xlabel('gyr_z')
    ax9.grid()

    plt.show()
