# Turbulenzmessung
Dieses Projekt wird im Rahmen der Lehrveranstaltung Messsysteme, der TH Köln im SoSe2021 bearbeitet.

__Projektbeschreibung__
Es behandelt die Turbulenzmessung mittels Trägheitsmesseinheit (Inertial Measurement Unit = IMU), welche in Radiosonden an Wetterballons angebracht werden und in die Atmosphäre aufsteigen.
Mithilfe der von den IMUs aufgenommenen Daten, können Rückschlüsse, sowohl auf die Stärke der Turbulenzen als auch die Höhe (turbulent region), in der dieses Auftreten, gezogen werden.

Das Projekt unterteilt sich in 3 Abschnitte:
1.	Aufbereitung empfangener Radiosonden Daten 
2.	Untersuchung von Bewegungsdaten eines Wetterballonsaufstiegs
3.	Vergleich verschiedener IMUs hinsichtlich der Tauglichkeit an in einer Radiosonde

----
## Software
Ziel des Projektes ist es, einen Radiosonde zu entwickeln, welche wir in die Atmosphäre steigen zu lassen, um eigene Daten über Turbulenzen aufzunehmen und auszuwerten.

__CSV-XDATA-Parser__
Im ersten Schritt werden die empfangenen XDATA vom Byte Format in lesbare Floats umgewandelt. Dabei werden die Daten auf mögliche CRC Fehler untersucht und fehlerhafte Datensätze gelöscht.

__CSV-XDATA-Combiner__
Mit diesem Skript können unterschiedliche XDATA Datensätze aus dem CSV-XDATA-Parsers anhand des Zeitstempels zusammengeführt werden.
Die 5 Messwerte pro Sekunde werden als Varianz ausgeben.

__CSV-RAW-RS41-Combiner__
Mit diesem Skript wird der RS41 Tracker Export um die XDATA ergänzt.

__CSV-Plotter__
Dieses Skript dient der Datenauswertung. Dafür werden als erstes mehre Höhendiagramme erstellt. Die Y-Achse verschiebt sich dabei auf allen Diagramen simultan um eine einfaches vergleichen bei einer bestimmten Höhe zu ermöglichen. 
Als nächstes wird die Kovarianzmatrix geplottet. Aus dieser lassen sich mögliche Zusammenhänge verschiedener Parameter erkennen.
----
##  Hardware

Es sollte ein Inertial Measurement Unit (IMU) gefunden werden die zusätzlich die Veränderungen des Magnetfeldes in 3 Richtungen erfasst. Die zuletzt benutzte IMU erfasste nur 6 Achsen. Die Preise stammen von octopart.com . Eine Vergleichstabelle und die Datenblätter befinden sich im Ordner Hardware.
Wir empfehlen den BMX160 da er kostengünstig ist und einen geringen Energieverbrauch hat.
