import numpy as np
import mltools as ml
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler  

X = np.genfromtxt('data/X_train.txt', delimiter = None) #100,000 data sets, 14 features
Y = np.genfromtxt('data/Y_train.txt', delimiter = None)
Xf = np.genfromtxt('data/X_test.txt', delimiter = None)
X,Y = ml.shuffleData(X,Y)

scaler = StandardScaler()  
scaler.fit(X) 

X = scaler.transform(X)  
Xf = scaler.transform(Xf)

Xtr = X[:80000,]
Ytr = Y[:80000,]

Xva = X[80001: 100000,]
Yva = Y[80001: 100000,]


nnTest = MLPClassifier(hidden_layer_sizes = (1000, 4), activation = 'logistic', solver = 'adam', 
                       learning_rate_init = 0.001) 


nnTest.fit(X,Y)

print("{0:>15}: {1:.4f}".format('Train AUC 2',nnTest.score(Xtr, Ytr)))
print("{0:>15}: {1:.4f}".format('Valid AUC 2',nnTest.score(Xva, Yva)))

kagle = nnTest.predict_proba(Xf)
Vali = nnTest.predict_proba(X)

Y_sub = np.vstack([np.arange(X.shape[0]), kagle[:, 1]]).T
Y_vali = np.vstack([np.arange(X.shape[0]), Vali[:, 1]]).T

np.savetxt('data/Y_sub.txt', Y_sub, '%d, %.5f', header='ID,Prob1', comments='', delimiter=',')
np.savetxt('data/Y_Vali.txt', Y_vali, '%d, %.5f', header='ID,Prob1', comments='', delimiter=',')
