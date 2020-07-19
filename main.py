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
        self.fitnessDic = {}
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
        print('parents: ', parent1, parent2)
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

    def mutation(self, parents, individual):
        parent1 = parents[0][1]
        parent2 = parents[1][1]
        random.seed()
        probability = random.random()
        if probability > 0.25:
            return individual       
        else:
            random.seed()
            probability = random.randint(0, 25)
            if probability > 0.5:
                mutatingElement = parent1
            else:
                mutatingElement = parent2

            if probability < (25/3):
                newKp = round(random.uniform(2,18),2)
                return [newKp, self.currentPopulation[mutatingElement][1], self.currentPopulation[mutatingElement][2]]
                
            elif probability < 2*(25/3):
                newTi = round(random.uniform(1.05, 9.42),2)
                return [self.currentPopulation[mutatingElement][0], newTi, self.currentPopulation[mutatingElement][2]]
                
            else:
                newTD = round(random.uniform(0.26, 2.37),2)
                return [self.currentPopulation[mutatingElement][0], self.currentPopulation[mutatingElement][1], newTD]
    

    def main(self):
        for generation in range(self.generations):
            calculatedParams = self.calculating_params(self.currentPopulation)
            self.fitness(calculatedParams)
            parents = self.selection()
            newPopulation = []
            for x in range(self.population):
                individual = self.crossover(parents)
                individual = self.mutation(parents, individual)
                newPopulation.append(individual)
            self.currentPopulation = newPopulation
        
        finalParets = parents
        parent1 = finalParets[0][1]
        print('FINAL ANSWER')
        print('Parent Index: ', parent1)
        print('Kp: ', self.currentPopulation[parent1][0])
        print('Ti: ', self.currentPopulation[parent1][1])
        print('Td: ', self.currentPopulation[parent1][2])
        print('ISE: ', calculatedParams[parent1][0])
        print('RiseTime: ', calculatedParams[parent1][1])
        print('SettlingTime: ', calculatedParams[parent1][2])
        print('OverShoot: ', calculatedParams[parent1][3])
        print('Fitness Value: ', self.fitnessDic[parent1])
        
        

        


attempt = Simulation(50, 150)