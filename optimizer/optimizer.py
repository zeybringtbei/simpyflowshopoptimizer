from random import random as rnd
from simpy import Environment
from flowshop import FlexibleJobShop, Station, MonitoredResource, StationRng
from numpy.random import default_rng
rng = default_rng()

class FlowShopOptimizer():

    def print_status(self, served, capacities, utilization):
        print("Served: {} - Capacities: {} - Utilization: {}".format(served,capacities,utilization))

    def carry_out_experiment(self, station_data: list, capacities: list, time_between_rng : StationRng, runtime: int):

        # Führt ein Simulationsexperiment durch und gibt Anzahl fertig gestellter Werkstücke und Maschinen
        # Auslastung zurück
        env = Environment()
        stations = [Station(station_data[i].name, MonitoredResource(env, capacities[i]), station_data[i].rng) for i in range(len(station_data))]
        jobShop = FlexibleJobShop(env, stations, False)
        env.process(self.sim_flowshop(env, jobShop, time_between_rng))
        env.run(until=runtime)
        nr_served = jobShop.nr_served
        utilization = jobShop.getUtilization()
        return nr_served, utilization

    def sim_flowshop(self, env: Environment, jobShop: FlexibleJobShop, timebetween: StationRng):
        
        # Simuliere den FlowShop, erzeuge sukzessive Werkstücke und speise sie in den Prozess ein
        count = 1
        while True:
            yield env.timeout(timebetween.getRandomNumber())  # Zwischenankunftszeit von Werkstücken
            env.process(jobShop.process_workpiece(count)) # Werkstück wird verarbeitet
            count += 1

    
class Hillclimber(FlowShopOptimizer):

    def optimize(self, time_between_arrivals: StationRng, station_data: list, iterations: int, runtime: int):
        
        best_capacities = [stat.cap for stat in station_data]
        best_nr_served, best_utilization = self.carry_out_experiment(station_data, best_capacities, time_between_arrivals, runtime)
        nr_served_inc = best_nr_served
        station_capacities = best_capacities[:]

        # Simulation ausführen
        improvement = True
        utilization = best_utilization[:]
        while(improvement):

            improvement = False
            # Erlaube mehrere Versuch der Verbesserung -> iterations=1 repräsentiert einen simplen HillClimber
            for _ in range(iterations):

                # Ermittle neue Kapazitäten
                new_caps = self.swap_caps_min_max_util(station_capacities, utilization)
                nr_served, utilization = self.carry_out_experiment(station_data, new_caps, time_between_arrivals, runtime)
                
                # Die aktuelle Lösung ist besser als die vorherige
                if nr_served > nr_served_inc:
                    station_capacities = new_caps
                    nr_served_inc = nr_served

                # Die aktuelle Lösung ist besser als die beste bekannte Lösung
                if nr_served > best_nr_served:
                    best_capacities = new_caps[:]
                    best_nr_served  = nr_served
                    best_utilization = utilization[:]
                    improvement = True
                    self.print_status(best_nr_served, best_capacities, best_utilization)

        return best_capacities, best_nr_served, best_utilization

    def swap_caps_min_max_util(self, capacities, stationUtilization):
        
        # Wähle mit höherer Wahrscheinlichkeit eine Ressource mit geringer Auslastung
        # und swappe deren Kapazität mit höherer Wahrscheinlichkeit zu einer
        # Ressource mit hoher Auslastung

        # Wähle Ressource mit tendenziel hoher Auslastung
        sortedUtil = [(i,v) for i,v in enumerate(stationUtilization)]
        sortedUtil = sorted(sortedUtil, key=lambda u : u[1], reverse=True)
        r = rnd()
        totalUtilization = 0
        insertIndex = -1
        sumutil = sum(stationUtilization)
        for e in sortedUtil:
            totalUtilization += e[1]/sumutil
            if totalUtilization >= r:
                insertIndex = e[0]
                break
        
        # Wähle Ressource mit tendenziell niedriger Auslastung
        removalIndex = -1
        totalNegUtilization = 0
        sumutil = sum([1-i for i in stationUtilization])
        sortedUtil = sorted(sortedUtil, key=lambda u : u[1])
        r = rnd()
        for e in sortedUtil:
            totalNegUtilization += (1-e[1])/sumutil
            if totalNegUtilization > r:
                removalIndex = e[0]
                break
        
        # Swappe die Kapazität
        caps_new = capacities[:]
        delta_a = -1 if capacities[removalIndex] > 1 else 0
        delta_b = delta_a*-1
        caps_new[removalIndex] = capacities[removalIndex] + delta_a
        caps_new[insertIndex] = capacities[insertIndex] + delta_b

        return caps_new