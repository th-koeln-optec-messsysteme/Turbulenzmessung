# Turbulenzmessung
Dieses Projekt wird im Rahmen der Lehrveranstaltung Messsysteme, der TH Köln im SoSe2021 bearbeitet.

__Projektbeschreibung__
Es behandelt die Turbulenzmessung mittels Trägheitsmesseinheit (Inertial Measurement Unit = IMU), welche in Radiosonden an Wetterballons angebracht werden und in die Atmosphäre aufsteigen.
Mithilfe der von den IMUs aufgenommenen Daten, können Rückschlüsse, sowohl auf die Stärke der Turbulenzen als auch die Höhe (turbulent region), in der dieses Auftreten, gezogen werden.

Das Projekt unterteilt sich in 3 Abschnitte:
1.	Aufbereitung empfangener Radiosonden Daten 
2.	Untersuchung von Bewegungsdaten eines Wetterballonsaufstiegs
3.	Vergleich verschiedener IMUs hinsichtlich der Tauglichkeit in einer Radiosonde

----

## Software

__01_CSV-XDATA-Parser__

Im ersten Schritt werden die empfangenen XDATA vom Byte Format in lesbare Floats umgewandelt. Dabei werden die Daten auf mögliche CRC Fehler untersucht und fehlerhafte Datensätze gelöscht. Zusätzlich wird die Varianz der IMU Daten berechnet. Die Anzahl der korrekten und fehlerhaften Datensätze wird ausgegeben.


__02_CSV-XDATA-Combiner__

Mit diesem Skript können unterschiedliche XDATA Datensätze aus dem 01_CSV-XDATA-Parsers anhand des Zeitstempels zusammengeführt werden.


__03_CSV-RAW-RS41-Combiner__

Mit diesem Skript wird der RS41 Tracker Export um die XDATA aus 02_CSV-XDATA-Combiner ergänzt.


__04_XDATA-Time-Subframer__

Hier werden die 5 IMU Messwerte pro Sekunde in auf Subframes aufgeteilt. Die RS41 Tracker Daten werden Dabei 5-mal kopiert und die Zeit in 0.2 Sekunden Schritten hoch gezählt. Es wird eine gesonderte Datei erstellt.


__05_CSV-IMU-Plotter__

Dieses Skript dient der Datenauswertung. Dafür werden als erstes mehre Höhendiagramme mit Daten aus dem RS41-Tracker erstellt. Die Y-Achse verschiebt sich dabei auf allen Diagramen simultan um eine einfaches vergleichen bei einer bestimmten Höhe zu ermöglichen. 
Als nächstes wird die Kovarianzmatrix geplottet. Aus dieser lassen sich mögliche zusammenhänge verschiedener Parameter erkennen.
Zum Schluss werden nochmals die ersten Höhendiagrame zusammen mit den IMU Daten aus den Subframes geplottet.


__06_CSV-Variance-Plotter__

Hier werden 10 Höhendiagrame geplottet aus dem RS41-Tracker und den 6 IMU Varianzen pro Sekunde.


Die folgenden Python-Pakete wurden in den Skripten benutzt:
struct, csv, os, operator, statistics, numpy, matplotlib.pyplot, matplotlib.ticker, pandas und seaborn

----

##  Hardware

Es sollte ein Inertial Measurement Unit (IMU) gefunden werden die zusätzlich die Veränderungen des Magnetfeldes in 3 Richtungen erfasst. Die zuletzt benutzte IMU erfasste nur 6 Achsen. Die Preise stammen von octopart.com. Eine Vergleichstabelle und die dazugehörigen Datenblätter befinden sich im Ordner Hardware.

Es gibt bis jetzt nur 3 nennenswerte Hersteller von 9 Achsen IMU-ICUs: Bosch, STMicroelectronics und Invensense. Diese IMUs oftmals für die Anwendung in einem Android Smartphone konzipiert für einen Temperaturbereich von -40°C bis +80°C. Andere Hersteller konzentrieren sich auf Sensoren für Flugzeuge z.B. Honeywell. Diese sind wesentlich genauer und haben auch einen erweiterten Betriebstemperaturbereich bis -54°C. Leider sind diese IMUs sehr teuer $1000+ und auch viel zu groß. IMUs für Temperaturen bis -65°C sind ansonsten nur noch im Militärbereich anzutreffen und unterliegen strengen Regulierungen. Bosch ist auch ein Lieferant für Militär IMUs.

Die von uns verglichenen IMUs besitzen alle einen eingebauten Mikrocontroller, der die Sensor Daten auswertet und es ermöglicht den Messbereich festzulegen. Die Messbereiche und die Empfindlichkeiten sind bei allen Sensoren ähnlich. Die größten Unterschiede sind im Energieverbrauch zu finden. Der BMX160 von Bosch ist dabei am sparsamsten und laut Bosch auch der kleinste derzeit verfügbare Chip.

Auf dem zweiten Platz liegt der ICM-20948 von Invensense. Für diesen Sensor ist ein Adafruit Board mit fertigen Bibliotheken verfügbar. https://www.adafruit.com/product/4554
Zudem ist der Sensor wesentlich günstiger und besitzt ein zusätzliches I2C interface an dem weitere Sensoren angeschlossen werden können.

Wir empfehlen den ICM-20948 von Invensense da er kostengünstig ist und einen geringen Energieverbrauch hat.
