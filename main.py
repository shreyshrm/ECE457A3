
"""
    Main
    1 [Start] Generate random population of n chromosomes (suitable solutions for the problem)
    2 [Fitness] Evaluate the fitness f(x) of each chromosome x in the population
    3 [New population] Create a new population by repeating following steps until the new population is complete
        3a[Selection] Select two parent chromosomes from a population according to their fitness (the better fitness, the bigger chance to be selected)
        3b[Crossover] With a crossover probability cross over the parents to form a new offspring (children). If no crossover was performed, offspring is an exact copy
        3c[Mutation] With a mutation probability mutate new offspring at each locus (position in chromosome).
        3d[Accepting] Place new offspring in a new population
    4 [Replace] Use new generated population for a further run of algorithm
    5 [Test] If the end condition is satisfied, stop, and return the best solution in current population
    6 [Loop] Go to step 2
"""
import random
import control


class Simulation:
    def __init__(self, population, generations):
        self.population = population
        self.generations = generations
        self.initialPopulation = self.initial_population()
        self.currentPopulation = self.initialPopulation
        self.fitnessDic = {}
        self.main()

    def initial_population(self):
        initialPopulationList = []
        random.seed()
        for individual in range(self.population):
            initialPopulationList.append([round(random.uniform(2,18), 2), round(random.uniform(1.05, 9.42), 2), round(random.uniform(0.26, 2.37), 2)])

        return initialPopulationList
    
    def calculating_params(self,populations):
        calculatedParams = []
        for population in populations:
            kp = population[0]
            ti = population[1]
            td = population[2]
            G = kp*control.tf([ti*td,ti,1],[ti,0])
            F = control.tf(1,[1,6,11,6,0])
            system = control.feedback(control.series(G,F), 1)

            t = []
            i = 0
            while i < 100:
                t.append(i)
                i += 0.01
        
            try:
                systemInfo = control.step_info(system)
            except IndexError:
                calculatedParams.append([10000000, 1, 100, 200])
                continue

            T, output = control.step_response(system, T=t)

            ISE = round(sum((output-1)**2),2)
            timeRise = round(systemInfo['RiseTime'],2)
            timeSettle = round(systemInfo['SettlingTime'],2)
            overshoot = round(systemInfo['Overshoot'],2)
            calculatedParams.append([ISE, timeRise, timeSettle, overshoot])

        return calculatedParams
        
    def fitness(self, calculatedParams):
        fitnessValues = []
        for x in range(self.population):
            ISE = calculatedParams[x][0]
            fitnessVal = 1/ISE
            self.fitnessDic[x] = fitnessVal 
        return

    def selection(self):
        #tournament style

        sortedFitnessDic = sorted([(v,k) for k,v in self.fitnessDic.items()])
        
        #keep 16 best parents
        for x in range(34):
            sortedFitnessDic.pop(0)

        tempList = []
        for x in range(8):
            y = 2*x
            random.seed()
            probability = random.random()
            if probability < 0.5:
                tempList.append(sortedFitnessDic[y])
            else:
                tempList.append(sortedFitnessDic[y+1])
        sortedFitnessDic = tempList

        tempList = []
        for x in range(4):
            y = 2*x
            random.seed()
            probability = random.random()
            if probability < 0.5:
                tempList.append(sortedFitnessDic[y])
            else:
                tempList.append(sortedFitnessDic[y+1])
        sortedFitnessDic = tempList

        tempList = []
        for x in range(2):
            y = 2*x
            random.seed()
            probability = random.random()
            if probability < 0.5:
                tempList.append(sortedFitnessDic[y])
            else:
                tempList.append(sortedFitnessDic[y+1])
        sortedFitnessDic = tempList
        

        parent1 = sortedFitnessDic[-1]
        parent2 = sortedFitnessDic[-2]
        return [parent1, parent2]

    def crossover(self, parents):
        parent1 = parents[0][1]
        parent2 = parents[1][1]
        random.seed()
        probability = random.random()
        if probability > 0.6:
            return self.currentPopulation[parent1]        
        else:
            if probability >= 0.5:
                return [self.currentPopulation[parent1][0], self.currentPopulation[parent1][1], self.currentPopulation[parent1][2]]
            elif probability >= 0.4:
                return [self.currentPopulation[parent2][0], self.currentPopulation[parent1][1], self.currentPopulation[parent1][2]]
            elif probability >= 0.3:
                return [self.currentPopulation[parent1][0], self.currentPopulation[parent2][1], self.currentPopulation[parent1][2]]
            elif probability >= 0.2:
                return [self.currentPopulation[parent1][0], self.currentPopulation[parent1][1], self.currentPopulation[parent2][2]]
            elif probability >= 0.1:
                return [self.currentPopulation[parent2][0], self.currentPopulation[parent1][1], self.currentPopulation[parent2][2]]
            else:
                return [self.currentPopulation[parent2][0], self.currentPopulation[parent2][1], self.currentPopulation[parent2][2]]

    # def mutation(self, parents, individual):
    #     parent1 = parents[0]
    #     parent2 = parents[1]
    #     random.seed()
    #     probability = random.random()
    #     if probability > 0.25:
    #         return self.currentPopulation[parents[0]]        
    #     else:
            


    def main(self):
        calculatedParams = self.calculating_params(self.initialPopulation)
        self.fitness(calculatedParams)
        for generation in range(1):
            parents = self.selection()
            newPopulation = []
            for x in range(self.population):
                individual = self.crossover(parents)
                print('individual: ', individual)
                # individual = self.mutation(parents, individual)
                # newPopulation.append(individual)

attempt = Simulation(50, 150)