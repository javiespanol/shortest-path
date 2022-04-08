import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from random import randint

#Para ejecutar poner en linea de comandos:
#   > python3 paths.py [fichero_configuracion]

#Fichero de configuración
# **Fichero .cfg**
#   1a Linea = Nodo inicial, cualquier entero correspondiente a algun nodo
#   2a Linea = 0 coste_enlace = 1 // 1 coste_enlace = [1-20](aleatorio)
#   3a Linea = 0 NO se ejecuta el esquema de los nodos(plot) // 1 SI se realiza el esquema de los nodos(plot)
#   4a Linea = Nombre del fichero que contiene la matriz de adyacencia
#   5a Linea = Lista de nodos por los que se desea pasar separados por ","

txt_file = open(sys.argv[1], "r")
next_ini = int(txt_file.readline())
coste_variable = int(txt_file.readline())
plot = int(txt_file.readline())
matriz_adyacencia = txt_file.readline()
matriz_adyacencia = matriz_adyacencia.replace("\n","")
file_content = txt_file.read()
q = file_content.split(",")
for t in range(len(q)):
    q[t]=int(q[t])
next=next_ini

#Variables auxiliares para el calculo del mínimo
l_min=99999
i_min=0
min=[]
fin=1

#Tramos a recorrer
recorrido=[]

#Trayectoria completa del camino a seguir
final=[]

#Matriz del .csv
input_data = pd.read_csv(matriz_adyacencia)
G = nx.Graph(input_data.values)

#Puesta aleatoria de los costes en funcion del .cfg
if coste_variable:
    for e in G.edges():
        G[e[0]][e[1]]['weight'] = randint(1, 20)


while len(q)>0:
    p = nx.shortest_path(G, source=next, weight='weight')

    for i in range(len(p)):
        if i not in q:
            p.pop(i)

    for k in p.keys():
        if len(p.get(k))<l_min:
            l_min=len(p.get(k))
            i_min=k
            min=p.get(k)

    next=i_min
    recorrido.append(min)
    q.pop(q.index(i_min))
    l_min=99999
    if len(q)==0 and fin:
        q.append(next_ini)
        fin=0

#Calculo de la longitud del trayecto, no del coste
sum=0
for n in recorrido:
    sum=sum+len(n)
    final=final[:-1]+n
sum=sum-len(recorrido)

print("Camino recorrido: ",final)
print("Saltos: ",sum)

if plot:
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G,with_labels=True)
    plt.show()