"""
Copyright: Dr. Lennart Zey 2022
Ein FlowShop Modell in SimPy.

Annahme: Es steht eine Gesamtkapazität, z.B. Arbeiter zur Verfügung, die beliebig 
auf einzelne Stationen, die von Werkstücken nacheinander besucht werden müssen,
verteilt werden können.

Ziel ist es eine Zuordnung von Arbeitern zu Stationen zu determinen, so dass die Anzahl erzeugter
Werkstücke möglichst hoch ist.

Dies geschieht in diesem Fall mit einem HillClimber Algorithmus bei dem sukzessive Kapazität von wenig
ausgelasteten Stationen zu stark ausgelasteten Stationen getauscht wird.
"""
from collections import namedtuple
from random import randint
from flowshop import StationRng
from optimizer import Hillclimber
from numpy.random import default_rng
rng = default_rng()


# | ----------------------------------------------
# | ---------------- MAIN ROUTINE ----------------
# | ----------------------------------------------
def generate_random_instance(nr_stations, max_cap):
    # Erzeuge eine zufällige Instanz
    Station = namedtuple("Station", "name cap rng")
    stations = [Station("Station {}".format(i), randint(1,max_cap), StationRng(rng.exponential, randint(1,8))) for i in range(nr_stations)]
    return stations

# Hyperparameter
TIME_BETWEEN = StationRng(rng.exponential, 2)
ITERATIONS = 20
RUNTIME = 2000

stations = generate_random_instance(nr_stations=10,max_cap=7)
opt = Hillclimber()
opt.optimize(time_between_arrivals=TIME_BETWEEN, station_data=stations, iterations=ITERATIONS, runtime=RUNTIME)



