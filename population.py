import snake as s
import numpy as np
import settings
import copy
import visualize

class population:
    def __init__(self):
        self.num_gen=1
        self.previous_generation= []
        self.current_generation= []
        for _ in range(settings.num_snakes_gen):
            self.current_generation.append(s.snake())
             
    def run(self):
        max_gen=0
        while max_gen<10:
            for i in self.current_generation:
                i.play()
            self.previous_generation=copy.copy(self.current_generation)
            self.current_generation=[]
            self.previous_generation.sort(key=lambda x: x.fitness,reverse=True)
            self.previous_generation=self.previous_generation[:settings.num_par_snakes]
            if settings.visualize:
                visualize.visualize(self.previous_generation[0])
            print("Gen:"+str(self.num_gen))
            avg=0
            for i in self.previous_generation:
                avg+=i.fitness/(settings.num_par_snakes+settings.num_snakes_gen)
            print("Average Fitness: "+str(avg))
            print("Best Fitness: "+str(self.previous_generation[0].fitness))
            most_fit_apple=len(self.previous_generation[0].eaten_apple_locations)
            print("Most Fit Apples Eaten: "+str(most_fit_apple))
            if most_fit_apple>=98:
                max_gen+=1
            parents= self.selection()
            for i in range(0,len(parents)-1,2):
                self.crossover(parents[i],parents[i+1])
            self.mutate()
            for i in self.previous_generation:
                self.current_generation.append(s.snake(i.network.weights,i.network.bias))
            self.num_gen+=1
        print("it worked?")
                 
    def selection(self):
        sum_=0
        for i in self.previous_generation:
            sum_+= i.fitness
        num=np.random.random_integers(0,sum_)
        parents=[]
        for _ in (range((settings.num_snakes_gen-settings.num_par_snakes))):
            current=0
            for i in self.previous_generation:
                current+= i.fitness
                if current>=num:
                    parents.append(i)
                    break
        return parents
        
            
    def crossover(self,x,y):
        
    #SBX
        c1_weights=[]
        c1_bias=[None]
        c2_weights=[]
        c2_bias=[None]
        for i in range(len(x.network.weights)):
            p1=x.network.weights[i]
            p2=y.network.weights[i]
            rand = np.random.uniform(0,1,p1.shape)
            gamma = np.empty(p1.shape)
            gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (settings.eta + 1))
            gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (settings.eta + 1))
            c1_weights.append(0.5 * ((1 + gamma)*p1 + (1 - gamma)*p2))
            c2_weights.append(0.5 * ((1 - gamma)*p1 + (1 + gamma)*p2))
        for i in range(1,len(x.network.bias)):
            p1=x.network.bias[i]
            p2=y.network.bias[i]
            rand = np.random.uniform(0,1,p1.shape)
            gamma = np.empty(p1.shape)
            gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (settings.eta + 1))
            gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (settings.eta + 1))
            c1_bias.append(0.5 * ((1 + gamma)*p1 + (1 - gamma)*p2))
            c2_bias.append(0.5 * ((1 - gamma)*p1 + (1 + gamma)*p2))
        self.current_generation.append(s.snake(c1_weights,c1_bias))
        self.current_generation.append(s.snake(c2_weights,c2_bias))
    
    #Code for SPBX (single point binary crossover)
        #c1_weights=copy.copy(p1.network.weights)
        #c2_weights=copy.copy(p2.network.weights)
        #c1_bias=copy.copy(p1.network.bias)
        #c2_bias=copy.copy(p2.network.bias)
        
        #for i in range(len(p1.network.weights)):
         #   rows,cols = p2.network.weights[i].shape
          #  row = np.random.randint(0, rows)
           # col = np.random.randint(0, cols)
            
           # c1_weights[i][:row, :] = p2.network.weights[i][:row, :]
            #c2_weights[i][:row, :] = p1.network.weights[i][:row, :]

            #c1_weights[i][:row, :col+1] = p2.network.weights[i][:row, :col+1]
            #c2_weights[i][:row, :col+1] = p1.network.weights[i][:row, :col+1]
        
        #for i in range(1,len(p1.network.bias)):
         #   rows=p1.network.bias[i].shape
          #  row = np.random.randint(0, rows)
           # for j in range(row,len(p1.network.bias)):
            #    c1_bias[i][j]=p2.network.bias[i][j]
             #   c2_bias[i][j]=p2.network.bias[i][j]
            
        #self.current_generation.append(s.snake(c1_weights,c1_bias))
        #self.current_generation.append(s.snake(c2_weights,c2_bias))
    
    def mutate(self):
    # gaussian
        for i in self.current_generation:
            for j in i.network.weights:
                mutation_array = np.random.random(j.shape) < settings.mutation_prob
                gaussian_mutation = np.random.normal(size=j.shape)
                gaussian_mutation[mutation_array] *= settings.gaussian_scale
                j[mutation_array] += gaussian_mutation[mutation_array]
            for j in i.network.bias:
                if j is not None:
                    mutation_array = np.random.random(j.shape) < settings.mutation_prob
                    gaussian_mutation = np.random.normal(size=j.shape)
                    gaussian_mutation[mutation_array] *= settings.gaussian_scale
                    j[mutation_array] += gaussian_mutation[mutation_array]

        # code for random uniform mutation
        #for i in self.current_generation:
         #   for j in i.network.weights:
          #      check=np.random.uniform(0,1,j.shape)
           #     for k in range(len(j)):
             
            #        for l in range(len(j[k])):
             #           if check[k][l]<settings.mutation_prob:
              #              j[k][l]+=np.random.uniform(-1,1)
            #for j in i.network.bias:
             #   if j is not None:
              #      check=np.random.uniform(0,1,j.shape)
               #     for k in range(len(j)):
                #        if check[k]<settings.mutation_prob:
                 #           j[k]+=np.random.uniform(-1,1)
        
        
                
                    
        
        
      
            
            
    
                
        
        
        
        
    

            