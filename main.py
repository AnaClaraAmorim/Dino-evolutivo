"""
Author: Ana Clara Amorim Andrade
"""
import sys
from classes.GameController import GameController
import weakref
args = sys.argv
"""
 3 modos padrões do jogo: Game, Simulation e Train
 Modo Game: O usuário pode competir contra os melhores dinos já treinados
 Modo Simulation: O usuário pode ver uma simulação do aprendizado dos dinos entre as gerações, partindo de um ponto inicial aleatório
 Modo Train: A partir da última geração pré treinada salva, continua o aprendizado do algoritmo
"""
if(args[1] in ['game', 'simulation', 'train']):
    dinos_per_gen = 10
    if(args[1] in ['simulation', 'train']):
        if(len(args)>2):
            dinos_per_gen = int(args[2])
    game = GameController(args[1], dinos_per_gen) # Inicia jogo
    f = weakref.finalize(game, game.saveGeneralRecord)
    game.run()
else:
    print('Command not found')