import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#Загружаем наши данные
df = pd.read_csv('actors.csv')
df1 = pd.read_csv("hahaton.csv", sep=",")

G = nx.Graph()

#Задаем вершины
course_list=df1['name'][20:70].unique()
for c in course_list:
  G.add_node(c, title=c,lable=c, color='blue')
  prof_list=df1['name'][20:70].unique()
for p in prof_list:
  G.add_node(p, title=p,lable=p, color='red')
  id_list=df1['title_id'][20:70].unique()
for i in id_list:
  G.add_node(i, title=i,lable=i, color='blue')

#Смотрим сколько получилось вершин
G.number_of_nodes()
#Пишем цикл для создания ребер
for i in id_list:
  for c in course_list:
    G.add_edge(c, i, color='black')
  for p in prof_list:
    G.add_edge(i, p, color='black')

#Рисуем граф
nx.draw(G)
