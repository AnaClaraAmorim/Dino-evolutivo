import numpy as np
#Essa classe representa a tomada de decisão dos dinos e realiza a mutação dos mesmos
class DinoBrain:
    def __init__(self, jumpAction = lambda x = None: x, bendAction = lambda x = None: x, raiseDino = lambda x = None: x, W = None, B = None):
        self.jumpAction = jumpAction #função que representa a tomada de decisão do pulo
        self.bendAction = bendAction #função que representa a tomada de decisão de se abaixar
        self.raiseDino = raiseDino #função que representa a tomada de decisão de ficar em pe
        if(W is None):
            self.W = np.random.uniform(-1, 1, (5,3))
        else:
            self.W = W
        if(B is None):
            self.B = np.random.uniform(-1, 1, (1,3))
        else:
            self.B = B
        
    def getMaxNode(self, Z):
        ind = np.unravel_index(np.argmax(Z, axis=None), Z.shape)
        return ind[1]

    #decide a ação que irá tomar   
    def takeAction(self, X):
        Z = np.matmul(X, self.W) + (self.B)
       
        with np.nditer(Z, op_flags=['readwrite']) as it:
            for item in it:
                if(item<0):
                    item[...] = 0
        output = self.getMaxNode(Z)

        if(output == 0):
            self.jumpAction(None)
        elif(output == 1):
            self.bendAction(None)
        elif(output == 2):
            self.raiseDino(None)

    def arithmeticRecombinationCrossOver(self, fittest):
        shape = fittest.shape
        parent1 = np.concatenate(fittest).ravel()
        chromosome = np.array([self.B, self.W],dtype=object)
        offspring = np.concatenate(chromosome).ravel()

        for i in np.arange(len(offspring)):
            gene1 = parent1[i]
            gene2 = offspring[i]

            [gene1, gene2] = [gene1, gene2] if gene1 > gene2 else [gene2, gene1]
            gene1 *= 1.1
            gene2 *= 0.9
            range = gene1 - gene2
            offspring[i] = gene2 + (np.random.rand() * range)

            
        self.B = offspring[:3].reshape(1, 3)
        self.W = offspring[3:].reshape(5, 3)
        #print("Dino: {}".format(self.B, self.W))

    #realiza mutação segundo distribuição normal
    def mutate(self, mutateRate):
        if(mutateRate != 0):
            self.W += np.random.uniform(-1, 1, (5,3))        
            self.B += np.random.uniform(-1, 1, (1,3))

    #cria um clone do dinossauro com possibilidade de mutação ou não    
    def getClone(self, mutationRate=0):
        brain = DinoBrain(self.jumpAction, self.bendAction, self.raiseDino, W=np.array(self.W), B=np.array(self.B))
        brain.mutate(mutationRate)
        return brain

    #salva o melhor dinossauro
    def save(self):
        np.save('data/brain/best_w.npy', self.W)
        np.save('data/brain/best_b.npy', self.B)

    def getBrain(self):
        return {
            "weight":self.W,
            "bias":self.B
        }
        
    #carrega o brain do melhor dinossauro
    def load(self):
        try:
            self.W = np.load('data/brain/best_w.npy')
            self.B = np.load('data/brain/best_b.npy')
            print("-------")
            print("w: ", self.W)
            print("b: ", self.B)
            print("-------")
        except IOError as err:
            return False
        return True