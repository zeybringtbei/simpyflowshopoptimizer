# Ein FlowShop Modell in SimPy

### Annahme
* Es gibt insgesamt n Stationen, die von Werkstücken nacheinander besucht werden müssen. 
*Die Bearbeitungszeit jedes Werkstücks auf der jeweiligen Station folgt einer Wahrscheinlichkeitsverteilung.
* Es steht eine Gesamtkapazität, z.B. Arbeiter zur Verfügung, die beliebig auf einzelne Stationen verteilt werden können. 
* Die Kapazität jeder Station entspricht der Anzahl Werkstücke, die gleichzeitig bearbeitet werden können. 
* Kommt ein Werkstück an einer Station mit voller Auslastung an, muss es warten bis das nächste Werkstück fertig gestellt ist.

### Ziel
Ziel ist es eine Zuordnung von Arbeitern zu Stationen zu bestimmen, so dass die Anzahl erzeugter
Werkstücke maximal ist.

### Verfahren
Dies geschieht in diesem Fall mit einem HillClimber Algorithmus bei dem sukzessive Kapazität von wenig
ausgelasteten Stationen zu stark ausgelasteten Stationen getauscht wird.



