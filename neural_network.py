import numpy as np
import settings
import copy


def sigmoid(num):
    return (1.0/(1.0+np.exp(-num)))

def relu(num):
    return max(0,num)
            
class network:
    
    def __init__(self,inherited_weights=None,inherited_bias=None):
        self.network_dimensions=settings.network_dimensions
        self.nodes=[]
        for _ in range(len(self.network_dimensions)):
            self.nodes.append(None)
        if inherited_weights is None:
            self.weights=[]
            for x in range(len(self.network_dimensions)-1):
                self.weights.append(np.random.uniform(-1,1,(self.network_dimensions[x+1],self.network_dimensions[x])))
        else:
            self.weights= inherited_weights
        if inherited_bias is None:
            self.bias=[]
            self.bias.append(None)
            for x in range(1,len(self.network_dimensions)):
                self.bias.append(np.random.uniform(-1,1,self.network_dimensions[x]))
        else:
            self.bias= inherited_bias
            
    def calculate_output(self):
        self.calculate_activation_values()
        max_indices= np.where(self.nodes[-1]==np.amax(self.nodes[-1]))
        return np.random.choice(max_indices[0])
        
    def calculate_activation_values(self):
        for layer in range(1,len(self.network_dimensions)):
            self.nodes[layer]=np.dot(self.weights[layer-1],self.nodes[layer-1])
            self.nodes[layer]+= self.bias[layer]
            if layer==len(self.nodes)-1:
                for x in self.nodes[layer]:
                    x= sigmoid(x)
            else:
                for x in self.nodes[layer]:
                    x= relu(x)