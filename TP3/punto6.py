import numpy as np

# Datos del problema

precios_x_elemento=np.array([100,20,115,25,200,30,40,100,100,100])
pesos_x_elemento=np.array([300,200,450,145,664,90,150,355,401,395])
npoblacion = 1000
peso_maximo=1000

#Variables auxiliares

poblacion = list()
padres = list()
poblacion_nueva = list()
precios_poblacion = list()
pesos_poblacion = list()
i=0

#Incializacion de la poblacion

while i<npoblacion:
    individuo = np.random.randint(0, 2, size=10)
    peso = np.sum(individuo*pesos_x_elemento)
    if peso>peso_maximo:
        continue
    else:
        precios_poblacion.append(np.sum(individuo*precios_x_elemento))
        pesos_poblacion.append(peso)
        poblacion.append(individuo)
        i+=1

# Algoritmo genetico, 1000 iteraciones con poblacion de 100 individuos da como resultado Precio total 300 . Aumentar la cantidad de inddividuos
# mejoró mucho el resultado.

#variables del algoritmo genetico
p_mutacion=0.3
generaciones=100
i=0

while i<generaciones:
    poblacion_nueva = list()
    padres = list()
    #calculo de ruleta de probabilidades y seleccion de poblacion nueva
    numeros = np.arange(npoblacion)
    probabilidad = precios_poblacion/np.sum(precios_poblacion)
    idxs = np.random.choice(numeros, size=npoblacion, replace=True, p=probabilidad)
    padres = [poblacion[i] for i in idxs]

    #seleccion de padres y cruza
    for j in range(0, npoblacion, 2):
        idxs2 = np.random.choice(numeros, size=2)
        padre1 = padres[idxs2[0]]
        padre2 = padres[idxs2[1]]
        punto_cruce = np.random.randint(1, 9)
        hijo1 = np.concatenate((padre1[:punto_cruce], padre2[punto_cruce:]))
        hijo2 = np.concatenate((padre2[:punto_cruce], padre1[punto_cruce:]))
        
        peso_hijo1 = np.sum(hijo1*pesos_x_elemento)
        peso_hijo2 = np.sum(hijo2*pesos_x_elemento)
        #mutacion generica y elitismo
        if np.random.rand() < p_mutacion:
            punto_mutacion = np.random.randint(0, 10)
            if hijo1[punto_mutacion] == 1:
                hijo1[punto_mutacion] = 0
            peso_hijo1 = np.sum(hijo1*pesos_x_elemento)
        if np.random.rand() < p_mutacion:
            punto_mutacion = np.random.randint(0, 10)
            if hijo2[punto_mutacion] == 1:
                hijo2[punto_mutacion] = 0
            peso_hijo2 = np.sum(hijo2*pesos_x_elemento)
        #mutacion solo si el peso del hijo supera el maximo
        while peso_hijo1 > peso_maximo:
            punto_mutacion = np.random.randint(0, 10)
            hijo1[punto_mutacion] = 1 - hijo1[punto_mutacion]
            peso_hijo1 = np.sum(hijo1*pesos_x_elemento)
        
        while peso_hijo2 > peso_maximo:
            punto_mutacion = np.random.randint(0, 10)
            hijo2[punto_mutacion] = 1 - hijo2[punto_mutacion]
            peso_hijo2 = np.sum(hijo2*pesos_x_elemento)
        poblacion_nueva.append(hijo1)
        poblacion_nueva.append(hijo2)
    poblacion=poblacion_nueva
    precios_poblacion = [np.sum(individuo*precios_x_elemento) for individuo in poblacion]
    pesos_poblacion = [np.sum(individuo*pesos_x_elemento) for individuo in poblacion]
    
    
    i+=1
#reordenamiento final de la poblacion
if len(poblacion_nueva) == npoblacion:
        sorted_indices = np.argsort(precios_poblacion)[-npoblacion:]
        poblacion = [poblacion[i] for i in sorted_indices]
        precios_poblacion = [precios_poblacion[i] for i in sorted_indices]
        pesos_poblacion = [pesos_poblacion[i] for i in sorted_indices]
print("Mejor individuo:", poblacion[npoblacion-1])
print("Precio total:", precios_poblacion[npoblacion-1])
print("Peso total:", pesos_poblacion[npoblacion-1])