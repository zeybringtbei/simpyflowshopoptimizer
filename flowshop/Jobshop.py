from .monitoredresource import MonitoredResource
from simpy import Environment
from colorama import Style, Fore

class StationRng(): 
    # A class that holds a certain type of random number generator
    # and its parameters
    def __init__(self,function, parameter):
        self.function = function
        self.parameter = parameter
    
    def getRandomNumber(self):
        return self.function(self.parameter)

class Station():
    # A station inside the flowshop, consisting of a resource,
    # a name and a StationRng
    def __init__(self, name: str, resource: MonitoredResource, rng: StationRng):
        self.name = name
        self.resource = resource
        self.rng = rng
    
    def processDuration(self):
        return self.rng.getRandomNumber()

class FlexibleJobShop():

    def __init__(self, env: Environment, stations, print: bool):
        self.print = print
        self.env = env
        self.nr_served = 0
        self.nr_entered = 0
        self.stations = stations

    def process_workpiece(self, id: int):
        
        # Verarbeitet die Worpieces Stück für Stück

        self.nr_entered += 1
        # Werkstücke durchlaufen die einzelnen Stationen (Arbeitsschritte)
        for station in self.stations:
            
            self.print_arrival(id, station)

            with station.resource.request() as request:
                yield request  # Werkstück wartet bis es dran ist
                duration = station.processDuration()
                yield self.env.timeout(duration) # Werkstück wird verarbeitet
                self.print_removal(id, station.name)

        self.print_finish(id)
        self.nr_served += 1
    
    def getUtilization(self):
        
        # Bestimmt durchschnittliche Auslastung jeder Maschine
        avg_util_stations = []
        for station in self.stations:
            avg_util = station.resource.avg_util()
            avg = sum([(i)*avg_util[i] for i in range(len(avg_util))])/station.resource.capacity
            avg_util_stations.append(round(avg,3))
        
        return avg_util_stations
    
    def print_arrival(self, id, station: Station):
        if self.print:
            print("{:.2f} - {} betritt {} (Queuecount: {})".format(self.env.now, id, station.name, len(station.resource.queue)))
    
    def print_removal(self, id, name):
        if self.print:
            print("{:.2f} - {} verlässt {}".format(self.env.now, id, name))

    def print_finish(self, id):
        if self.print:
            print(Style.BRIGHT + Fore.GREEN + "{:.2f} - Produkt {} ist fertig!".format(self.env.now, id) + Style.RESET_ALL) 