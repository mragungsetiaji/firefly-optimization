from math import exp
import numpy as np
import pandas as pd

individu = np.array([
    [ 4, 12,  4,  5,  2,  8,  4,  4,  4, 13,  4,  2,  2,  7,  2, 11, 3, 15,  2,  3,  4,  9,  1,  6,  2,  1,  1, 14,  4, 10],
    [ 3, 15,  1, 14,  1,  9,  2,  4,  1,  5,  4, 11,  3, 10,  2,  1, 1,  3,  4,  8,  3,  6,  1, 13,  1,  7,  3, 12,  3,  2],
    [ 1, 11,  4,  4,  1,  6,  4,  7,  3, 12,  4, 10,  2, 14,  3,  1, 1, 13,  2, 15,  3,  9,  4,  8,  3,  5,  1,  2,  4,  3],
    [ 2, 14,  3, 13,  4, 10,  1,  3,  1,  8,  2, 11,  4,  7,  2,  1, 4,  9,  3,  5,  4, 15,  3, 12,  4,  4,  1,  6,  1,  2],
    [ 3,  9,  3, 13,  2,  3,  3,  1,  4,  6,  1, 11,  3,  8,  4, 10, 3, 14,  1,  5,  3,  2,  3, 12,  3, 15,  3,  7,  3,  4],
    [ 4,  2,  1,  8,  3, 15,  4,  6,  3,  3,  4, 10,  1, 11,  1,  7, 3, 12,  4,  4,  4,  1,  2, 14,  1,  9,  3, 13,  3,  5],
    [ 2,  1,  4,  6,  2,  4,  1,  3,  1,  7,  2,  8,  4,  5,  2, 12, 4, 15,  4, 10,  2, 14,  4,  2,  1, 13,  2, 11,  1,  9],
    [ 4,  3,  1,  8,  2,  1,  3, 15,  3, 12,  1,  2,  1, 10,  1,  4, 3, 13,  2, 14,  4,  5,  1,  7,  3, 11,  2,  6,  1,  9],
    [ 4, 15,  4, 10,  3,  7,  2, 11,  2,  9,  2,  1,  1,  4,  2,  8, 2, 14,  2,  3,  2, 12,  3,  6,  4, 13,  4,  5,  4,  2]
    ])

data_outlet = pd.read_csv("data_outlet.csv")
"""data_outlet
"Nama Outlet | Latitude | Longitude | Open Time | Close Time | Accessibility | Demand"
"""

class Firefly(object):
    """
    Firefly Algorithm
    """

    def __init__(self, individu, data_outlet):

        self.X = individu
        self.gamma = 0.95
        self.number_outlet = len(data_outlet)
        self.data_outlet = data_outlet
        self.fitness_outlet = get_fitness_outlet() 

        # fleet
        self.fleet_dict = {"Truck":1, "Van":2, "Triseda":3, "Motor":4}
        self.fleet_capacity = [30, 15, 7, 3]

    def get_x_fcs(self):
        # variable x untuk fcs setiap column (total demand/fleet capacity)
        # bentuknya list sebanyak X

        x_fcs = []
        for i in self.X:
            total_demand, total_capacity = 0, 0
            for j in range(len(i)):
                if j % 2 == 0:
                    total_capacity = total_capacity + self.fleet_capacity[i[j]]
                else:
                    total_demand = total_demand + self.data_outlet["Demand"][i[j]]
            x_fcs.append(total_demand/total_capacity)
        return x_fcs

    def get_x_oas(self):
        # variable x untuk oas setiap column match(accessibily <> fleet)
        # bentuknya list sebanyak X

        self.data_outlet.replace({"accessibility":self.fleet_dict})
        list_access = list(self.data_outlet["accessibility"])
        
        x_oas = []
        for i in self.X:
            is_match = 0
            for j in range(len(i)):
                if j % 2 != 0:
                    if list_access[i[j + 1]] ==  i[j]:
                        is_match = is_match + 1
            x_oas.append(is_match/(len(i)/2))
        return x_oas

    def fitness_fcs(self, x):
        """
            Fleet Capacity Score (FCS)
        """
        k, x0 = 15, 0.5
        return 1/(1 + exp(-k*(x-x0)))
        
    def fitness_odws(self, x):
        """
            Outlet Delivery Window Score (ODWS)
        """
        return x^3*(self.number_outlet - 
                        (x*(self.number_outlet-1)/100)
                    )

    def fitness_fdws(self, x):
        """
            Fleet Delivery Window Score (FDWS)
        """
        k, x0 = -10, 0.5
        return 1/(1 + exp(-k*(x-x0)))

    def fitness_oas(self, x):
        """
            Outlet Accessibility Score (OAS)
        """
        return x^3

    def get_fitness_outlet(self, x):
        # Total fitness
        return (fitness_fcs(x) + fitness_odws(x) +
                fitness_fdws(x) + fitness_oas(x))
    
    def hamming_distance(c1, c2):
        # Hamming Distance
        if len(c1) != len(c2):
            raise ValueError("Panjang kedua cluster tidak sama!")
        count = 0
        for i in range(len(c1)):
            count += (c1[i] != c2[i])
        return count
    
    def random(self, r_ij):
        # Random number antara 2 dan r_ij
        return np.random.randint(low=2, r_ij*self.gamma, size=1)

    def fly(self):



