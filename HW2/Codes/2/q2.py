# -*- coding: utf-8 -*-
"""Q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IY-0BAvOf1b775TrvrKeCNySv4B0EFqW
"""

!pip install EoN

import networkx as nx
import EoN
import matplotlib.pyplot as plt
import pandas as pd

"""2.1"""

def load_data_for_q1_3_2(filename):
    """
    Helper function for Question 1.3.2
    Takes in a filename of the data that contains src, target pairs, that are 
separated by some blank chars, with no header info (e.g., no column name provided)
    Returns the dataframe of node pairs and the undirected graph G
    >>> filename = "datasets/q1.3.2/example.txt"
    >>> df_data, G = load_data_for_q1_3_2(filename)
    >>> print("df_data shape: {}".format(df_data.shape))
    df_data shape: (4950, 2)
    >>> print("df_data first 5 rows: \n{}".format(df_data.head()))
    df_data first 5 rows:
    src  dst
    0    2    1
    1    3    1
    2    3    2
    3    4    1
    4    4    2
    >>> print("Information on G. \n{}".format(nx.info(G)))
    Information on G.
    Name:
    Type: Graph
    Number of nodes: 100
    Number of edges: 4950
    Average degree:  99.0000
    """
    df_data = pd.read_csv(filename, header=None, delimiter=r"\s+", names=["src", 
"dst"])
    print(len(df_data))
    # Construct networkx graph object
    G = nx.from_pandas_edgelist(df_data, "src", "dst")
    
    print(len(G.edges))
    # Returns the dataframe and the networkx graph object
    return G

def load_seq_data():

  # How to read from a file. Note: if your egde weights are int, 
  # change float to int.
  G=[]
  i=1
  while i<10:
    PATH='/content/network'+str(i)+'.txt'
    print(PATH)
    Graphtype=nx.Graph()   # use net.Graph() for undirected graph

    # How to read from a file. Note: if your egde weights are int, 
    # change float to int.
    g = nx.read_edgelist(
      PATH, 
      create_using=Graphtype,
      nodetype=int,
      data=(('weight',float),)
      )

    G.append(g)
    i+=1
  edges1=[]
  for i in range(len(G)):
    edges1=edges1+list(G[i].edges)
    print(len(edges1))
  
  for i in range(len(edges1)):
    edges1[i]=tuple(edges1[i])
  counts = dict()
  for (i,j) in edges1:
    if ((i,j) not in counts) and ((j,i) not in counts):
      counts[(i,j)] = 1
    else:
      counts[(i,j)]=max(counts.get((i,j), 0), counts.get((j,i), 0)) +1

  df=pd.DataFrame()
  maps=list(counts.keys())
  vals=list(counts.values())
  df['v1']=[m[0] for m in maps]
  df['v2']=[m[1] for m in maps]
  df['val']=[v for v in vals]

  return df

def adj_eig(df,rho):
  from scipy.sparse.linalg import eigsh
  df=df[df['val']>=rho]
  df=df.reset_index(drop=True)
  #G=nx.Graph()
  print(len(df))
  G = nx.from_pandas_edgelist(df, 'v1','v2')
  A = nx.adjacency_matrix(G)
  A = A.asfptype()
  e,_ = eigsh(A, k=1,which='LM')
  return max(e)

from tqdm import tqdm
df=load_seq_data()
rholist=[1,2,3,4,5,6,7,8,9]
#rholist=[1]
eiglist=[]
for rho in tqdm(rholist):
  eiglist.append(adj_eig(df,rho))

plt.plot(rholist, eiglist)
plt.xlabel("rho")
plt.ylabel("lambda")
plt.savefig('rho_lam.png')

"""2.2"""

def graph_create(df,rho):
  from scipy.sparse.linalg import eigs
  df=df[df['val']>=rho]
  df=df.reset_index(drop=True)
  #G=nx.Graph()
  print(len(df))
  G = nx.from_pandas_edgelist(df, 'v1','v2')
  return G



G=graph_create(df,1)
Ilist=[]
Slist=[]
Tlist=[]
sis_out=pd.DataFrame()
for i in range(10):
  gamma = 0.08
  tau = 0.001
  data = EoN.fast_SIS(G, tau, gamma, tmax = 10,
                            initial_infecteds = [1],return_full_data=True)
  il=[]
  sl=[]
  tl=[]
  for j in range(11):
    
    status = data.get_statuses(G.nodes,j)
    infected = [node for node, status in status.items() if status == "I"]
    il.append(len(infected))
    recovered = [node for node, status in status.items() if status == "S"]
    sl.append(len(recovered))
    tl.append(j)
  #Ilist.append(il)
  #Slist.append(sl)
  #Tlist.append(tl)
  if len(sis_out)==0:
    sis_out['t']=tl
    sis_out['S']=sl
    sis_out['I']=il
    #sir_out['R']=R
    
  else:
    sis_out['S1']=sl
    sis_out['I1']=il
    #sir_out['R1']=R
    sis_out['S']=sis_out['S']+sis_out['S1']
    sis_out['I']=sis_out['I']+sis_out['I1']
    #sir_out['R']=sir_out['R']+sir_out['R1']
    #print(sir_out)
sis_out['S']=sis_out['S']/50
sis_out['I']=sis_out['I']/50
#sis_out['R']=sir_out['R']/50

sis_out

import matplotlib.pyplot as plt
#sline = plt.plot("t","S","",data=sis_out,color="blue",linewidth=2)
iline = plt.plot("t","I","",data=sis_out,color="red",linewidth=2)
#rline = plt.plot("t","R","",data=sir_out,color="blue",linewidth=2)
plt.xlabel("Time",fontweight="bold")
plt.ylabel("Number",fontweight="bold")
legend = plt.legend(title="Population",loc=5,bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
plt.savefig('SIS_1.png')

G=graph_create(df,1)
Ilist=[]
Slist=[]
Tlist=[]
sis_out=pd.DataFrame()
for i in range(50):
  gamma = 0.08
  tau = 0.0001
  data = EoN.fast_SIS(G, tau, gamma, tmax = 10,
                            initial_infecteds = [1],return_full_data=True)
  il=[]
  sl=[]
  tl=[]
  for j in range(11):
    
    status = data.get_statuses(G.nodes,j)
    infected = [node for node, status in status.items() if status == "I"]
    il.append(len(infected))
    recovered = [node for node, status in status.items() if status == "S"]
    sl.append(len(recovered))
    tl.append(j)
  #Ilist.append(il)
  #Slist.append(sl)
  #Tlist.append(tl)
  if len(sis_out)==0:
    sis_out['t']=tl
    sis_out['S']=sl
    sis_out['I']=il
    #sir_out['R']=R
    
  else:
    sis_out['S1']=sl
    sis_out['I1']=il
    #sir_out['R1']=R
    sis_out['S']=sis_out['S']+sis_out['S1']
    sis_out['I']=sis_out['I']+sis_out['I1']
    #sir_out['R']=sir_out['R']+sir_out['R1']
    #print(sir_out)
sis_out['S']=sis_out['S']/50
sis_out['I']=sis_out['I']/50
#sis_out['R']=sir_out['R']/50

import matplotlib.pyplot as plt
#sline = plt.plot("t","S","",data=sis_out,color="blue",linewidth=2)
iline = plt.plot("t","I","",data=sis_out,color="red",linewidth=2)
#rline = plt.plot("t","R","",data=sir_out,color="blue",linewidth=2)
plt.xlabel("Time",fontweight="bold")
plt.ylabel("Number",fontweight="bold")
legend = plt.legend(title="Population",loc=5,bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
plt.savefig('SIS_2.png')

"""2.3"""

G=graph_create(df,1)

from scipy.sparse.linalg import eigsh
beta = 0.01
gamma = 0.16
A = nx.adjacency_matrix(G)
A = A.asfptype()
e,_ = eigsh(A, k=1,which='LM')
max_lambda=max(e)
strength=max_lambda*beta/gamma
removed=0
node_id=[]
strength_pl=[]
deg_pl=[]
G_a=G
while (strength>=1):
  strength_pl.append(strength)
  deg_tup=sorted(G_a.degree, key=lambda x: x[1], reverse=True)[0]
  rem_node=deg_tup[0]
  deg_pl.append(deg_tup[1])
  G_a.remove_node(rem_node)
  removed+=1
  A = nx.adjacency_matrix(G_a)
  A = A.asfptype()
  e,_ = eigsh(A, k=1,which='LM')
  max_lambda=max(e)
  strength=max_lambda*beta/gamma

strength_df=pd.DataFrame()
strength_df['strength']=strength_pl
strength_df['removed']=[(i+1) for i in range(len(strength_pl))]

import matplotlib.pyplot as plt
#sline = plt.plot("t","S","",data=sis_out,color="blue",linewidth=2)
sline = plt.plot("removed","strength","",data=strength_df,color="green",linewidth=2)
#rline = plt.plot("t","R","",data=sir_out,color="blue",linewidth=2)
plt.xlabel("Number of Nodes Removed",fontweight="bold")
plt.ylabel("Strength",fontweight="bold")
#legend = plt.legend(title="Population",loc=5,bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
plt.savefig('strength.png')

"""2.4"""

from scipy.sparse.linalg import eigsh
beta = 0.01
gamma = 0.16
A = nx.adjacency_matrix(G)
A = A.asfptype()
e,_ = eigsh(A, k=1,which='LM')
max_lambda=max(e)
strength=max_lambda*beta/gamma
removed=0
node_id=[]
strength_pl=[]
deg_pl=[]
G_a=G
G_b=G_a
while (strength>=1):
  strength_pl.append(strength)
  deg_tup=sorted(G_a.degree, key=lambda x: x[1], reverse=True)[0]
  rem_node=deg_tup[0]
  deg_pl.append(deg_tup[1])
  G_a.remove_node(rem_node)
  removed+=1
  A = nx.adjacency_matrix(G_a)
  A = A.asfptype()
  e,_ = eigsh(A, k=1,which='LM')
  max_lambda=max(e)
  strength=max_lambda*beta/gamma
  if strength>1:
    G_b=G_a

len(G_b.nodes)

import random
Ilist=[]
Slist=[]
Tlist=[]
sis_out=pd.DataFrame()
sis_out1=pd.DataFrame()
sis_out2=pd.DataFrame()
init_node=random.choice(list(G_a.nodes()))
for i in range(100):
  gamma = 0.01
  tau = 0.16
  data = EoN.fast_SIS(G, tau, gamma, tmax = 10,
                            initial_infecteds = init_node,return_full_data=True)
  il=[]
  sl=[]
  tl=[]
  for j in range(11):
    
    status = data.get_statuses(G.nodes,j)
    infected = [node for node, status in status.items() if status == "I"]
    il.append(len(infected))
    recovered = [node for node, status in status.items() if status == "S"]
    sl.append(len(recovered))
    tl.append(j)
  #Ilist.append(il)
  #Slist.append(sl)
  #Tlist.append(tl)
  if len(sis_out)==0:
    sis_out['t']=tl
    sis_out['S']=sl
    sis_out['I']=il
    #sir_out['R']=R
    
  else:
    sis_out['S1']=sl
    sis_out['I1']=il
    #sir_out['R1']=R
    sis_out['S']=sis_out['S']+sis_out['S1']
    sis_out['I']=sis_out['I']+sis_out['I1']
    #sir_out['R']=sir_out['R']+sir_out['R1']
    #print(sir_out)
sis_out1['S']=sis_out['S']/100
sis_out1['I']=sis_out['I']/100
#sis_out['R']=sir_out['R']/50

sis_out1

sis_out1['t']=tl

sis_out=pd.DataFrame()
Ilist=[]
Slist=[]
Tlist=[]
for i in range(100):
  gamma = 0.01
  tau = 0.16
  data = EoN.fast_SIS(G_b, tau, gamma, tmax = 10,
                            initial_infecteds = init_node,return_full_data=True)
  il=[]
  sl=[]
  tl=[]
  for j in range(11):
    
    status = data.get_statuses(G_b.nodes,j)
    infected = [node for node, status in status.items() if status == "I"]
    il.append(len(infected))
    recovered = [node for node, status in status.items() if status == "S"]
    sl.append(len(recovered))
    tl.append(j)
  #Ilist.append(il)
  #Slist.append(sl)
  #Tlist.append(tl)
  if len(sis_out)==0:
    sis_out['t']=tl
    sis_out['S']=sl
    sis_out['I']=il
    #sir_out['R']=R
    
  else:
    sis_out['S1']=sl
    sis_out['I1']=il
    #sir_out['R1']=R
    sis_out['S']=sis_out['S']+sis_out['S1']
    sis_out['I']=sis_out['I']+sis_out['I1']
    #sir_out['R']=sir_out['R']+sir_out['R1']
    #print(sir_out)
sis_out2['S']=sis_out['S']/100
sis_out2['I']=sis_out['I']/100
#sis_out['R']=sir_out['R']/50

sis_out2['t']=tl

import matplotlib.pyplot as plt
#sline = plt.plot("t","S","",data=sis_out,color="blue",linewidth=2)
iline = plt.plot("t","I","",data=sis_out1,color="red",linewidth=2)
#rline = plt.plot("t","R","",data=sir_out,color="blue",linewidth=2)
plt.xlabel("Time",fontweight="bold")
plt.ylabel("Number",fontweight="bold")
legend = plt.legend(title="Population",loc=5,bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
plt.savefig('SIS_small.png')

import matplotlib.pyplot as plt
#sline = plt.plot("t","S","",data=sis_out,color="blue",linewidth=2)
iline = plt.plot("t","I","",data=sis_out2,color="blue",linewidth=2)
#rline = plt.plot("t","R","",data=sir_out,color="blue",linewidth=2)
plt.xlabel("Time",fontweight="bold")
plt.ylabel("Number",fontweight="bold")
legend = plt.legend(title="Population",loc=5,bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
plt.savefig('SIS_big.png')

removed