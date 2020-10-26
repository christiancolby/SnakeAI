
#SETTINGS
network_dimensions=(32,20,12,4) #32 and 4 should always be the first and last numbers
game_size=10 #the dimensions of the game
num_snakes_gen=1500 # the number of snakes in one generation
num_par_snakes=500 #num_snakes to be carried over between gens
vision_directions=8 #don't change this, functionality for more or less directions hasn't been added
lifespan=1000 # the maximum number of generations a snake can participate in
eta=100 # effects the weights of the snakes during crossover. The higher the eta, the closer the weights of the offspring snakes will be with the parent snakes
mutation_prob=.05 #dictates the chance that a snake will mutate
gaussian_scale=.3 #determines how much each snake will mutate when they do
visualize=True # if this is true after every generation the game of the snake with the highest fitness will be replayed







    
        