import numpy as np
import matplotlib.pyplot as plt

Y_BestScore = np.load('data/general/best_scores.npy')

X_Geracoes = np.arange(Y_BestScore.shape[0])

Y_AverageScore = np.load('data/general/average_scores.npy')



plt.plot(X_Geracoes, Y_BestScore, label="Melhor score", linestyle='dashed', linewidth = 1,
         marker='o', markerfacecolor='blue', markersize=4)
plt.plot(X_Geracoes, Y_AverageScore, label="Média score", linestyle='dashed', linewidth = 1,
         marker='o', markerfacecolor='red', markersize=4)

# naming the x axis
plt.xlabel('Gerações')
# naming the y axis
plt.ylabel('Score')
# giving a title to my graph
plt.title('Melhor score e Média de pontuação por geração')
  
# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()