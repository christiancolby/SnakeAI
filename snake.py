import numpy as np
import collections as col
import neural_network as net
import settings
import copy
import itertools

def distance(x,y):
    return np.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))

def contains(point,array):
    for i in array:
        if np.array_equal(i,point):
            return True
    return False

class snake:
    
    def __init__(self,inherited_weights=None,inherited_bias=None):
        if inherited_weights is None and inherited_bias is None:
            self.network= net.network()
        else:
            self.network=net.network(inherited_weights,inherited_bias)
        self.dimensions= settings.game_size
        self.body_locations= col.deque()
        self.body_locations.append(np.random.random_integers(3,self.dimensions,2))
        self.body_locations.append(np.array([self.body_locations[0][0],self.body_locations[0][1]-1]))
        self.body_locations.append(np.array([self.body_locations[0][0],self.body_locations[0][1]-2])) #this one gets popped on the first run through the while loop so the snake effectively starts at length two
        self.all_body_locations=col.deque()
        self.all_body_locations.append(copy.copy(self.body_locations))
        #head is index 0
        self.eaten_apple_locations=[]
        self.current_apple_location=np.random.random_integers(1,self.dimensions,2)
        while contains(self.current_apple_location,self.body_locations):
            self.current_apple_location=np.random.random_integers(1,self.dimensions,2)
        #apple locations are stored for replay purposes
        self.starting_apple_location=copy.copy(self.current_apple_location)
        self.head_direction=np.array([0,0,0,0]) #U,D,R,L
        self.head_direction[np.random.random_integers(0,3)]=1
        self.direction_list=[]
        self.direction_list.append(copy.copy(self.head_direction))
        self.tail_direction=np.array([1,0,0,0])#because the tail always starts one below the head
        self.wall_vision=np.empty(settings.vision_directions) #8-way vision starting at 12 o clock going clockwise
        self.apple_vision=np.empty(settings.vision_directions)
        self.body_vision=np.empty(settings.vision_directions)
        self.vision_slopes=np.array([[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]])
        self.steps_taken=-1
        self.steps_since_last_apple=-1
        self.fitness=None
        
    def is_alive(self):
        if (self.body_locations[0][0]>self.dimensions or self.body_locations[0][0]<1 or self.body_locations[0][1]>self.dimensions or self.body_locations[0][1]<1):
            return False
        if (contains(self.body_locations[0],itertools.islice(self.body_locations,1,None))):
            return False
        else:
            return True
            
    def determine_tail_direction(self):
        self.tail_direction=np.zeros(4)
        last=len(self.body_locations)-1
        dif= np.subtract(self.body_locations[last-1],self.body_locations[last])
        if np.array_equal(dif,np.array([0,1])):
            self.tail_direction[0]=1
        elif np.array_equal(dif,np.array([0,-1])):
            self.tail_direction[1]=1
        elif np.array_equal(dif,np.array([1,0])):
            self.tail_direction[2]=1
        elif np.array_equal(dif,np.array([-1,0])):
            self.tail_direction[3]=1
        
    def move_head(self):
        if self.head_direction[0]==1:
            self.body_locations.appendleft(np.add(self.body_locations[0],np.array([0,1])))
        if self.head_direction[1]==1:
            self.body_locations.appendleft(np.add(self.body_locations[0],np.array([0,-1])))
        if self.head_direction[2]==1:
            self.body_locations.appendleft(np.add(self.body_locations[0],np.array([1,0])))
        if self.head_direction[3]==1:
            self.body_locations.appendleft(np.add(self.body_locations[0],np.array([-1,0])))
                
    def update_vision(self):
        self.wall_vision=np.zeros(settings.vision_directions) 
        self.apple_vision=np.zeros(settings.vision_directions)
        self.body_vision=np.zeros(settings.vision_directions)
        for i in range(settings.vision_directions):
            point=copy.copy(self.body_locations[0])
            distance=0
            while self.wall_vision[i]== 0:
                point=np.add(point,self.vision_slopes[i])
                distance+=1
                apple_seen=False
                body_seen=False
                if apple_seen==False and np.array_equal(point,self.current_apple_location):
                    apple_seen=True
                    self.apple_vision[i]=1/distance   
                if body_seen==False and (contains(point,self.body_locations) and self.body_vision[i]==0):
                    body_seen=True
                    self.body_vision[i]=1/distance 
                if ((point[0]>self.dimensions or point[0]<1 or point[1]>self.dimensions or point[1]<1) and self.wall_vision[i]==0):
                    self.wall_vision[i]=1/ distance 
                        
    def update_network_inputs(self):
        self.network.nodes=[]
        for _ in range(len(settings.network_dimensions)):
            self.network.nodes.append(None)
        vision=np.zeros(settings.vision_directions*3)
        for i in range(settings.vision_directions):
            vision[(i*3)]=self.wall_vision[i]
            vision[(i*3)+1]=self.apple_vision[i]
            vision[(i*3)+2]=self.body_vision[i]
        self.network.nodes[0]=np.hstack((vision,self.head_direction,self.tail_direction))
        
    def make_decision(self):
        direction=self.network.calculate_output()
        self.head_direction=np.zeros(4)
        self.head_direction[direction]=1
        self.direction_list.append(direction)
            
    def update_apple(self):
        self.eaten_apple_locations.append(self.current_apple_location)
        possible_locations=[]
        for i in range(1,self.dimensions+1):
            for j in range(1,self.dimensions+1):
                point=[i,j]
                if not (contains(point,self.body_locations)):
                    possible_locations.append(point)
        self.current_apple_location=(possible_locations[np.random.random_integers(0,len(possible_locations)-1)])
        self.steps_since_last_apple=0
            
    def calculate_fitness(self):
        x=self.steps_taken
        y=len(self.eaten_apple_locations)
        return (x) + ((2**y) + (y**2.1)*500) - (((.25 * x)**1.3) * (y**1.2))
        
    def play(self):
        while (self.steps_since_last_apple<settings.lifespan and self.is_alive() and len(self.eaten_apple_locations)<((self.dimensions**2)-2)):
            self.steps_taken+=1
            self.steps_since_last_apple+=1
            if (np.array_equal(self.body_locations[0],self.current_apple_location)):
                self.update_apple()
            else:
                self.body_locations.pop()
            self.update_vision()
            self.update_network_inputs()
            self.make_decision()
            self.determine_tail_direction()
            self.move_head()
            self.all_body_locations.append(copy.copy(self.body_locations))
        self.fitness=self.calculate_fitness()
            
            
            
        
    
    
        
        
        
        
        