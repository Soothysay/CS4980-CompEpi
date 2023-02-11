# -*- coding: utf-8 -*-
"""Q1.3.3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x957OIi-q6_xqqQkxYyuFXq4bGgUEGLP
"""

# -*- coding: utf-8 -*-
"""Q1.3.3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x957OIi-q6_xqqQkxYyuFXq4bGgUEGLP
"""

import pandas as pd
df=pd.read_csv('/content/COVID19_GA.csv')

df

import matplotlib.pyplot as plt
z=df['deaths'].tolist()
y=[]
x=[]
for i in range(len(z)):
  y.append((z[i])) 
for i in range((len(y))):
  x.append(i) 
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
ydata = np.array(y, dtype=float)
xdata = np.array(x, dtype=float)

def SIR(y, x,beta,gamma,N):
    ds=-1.0*beta*y[0]*y[1]/N
    di=(beta*y[0]*y[1]/N)-(gamma*y[1])
    dr=gamma*y[1]
    return ds,di,dr
def FitSIR(x, beta,gamma):
    S0 = N - I0
    ret =  integrate.odeint(func = SIR, y0 = (S0, I0, 0.002039), t = x, args = (beta, gamma, N))
    return ret[:,2]
    #I = N - ret[:,0]
    #R = R+ret[:,2]
    #R=np.gradient(R)
    #return R
    
N=1 #Total population 
I0=0.107980
ParaOpt, ParaCov = optimize.curve_fit(f = FitSIR, xdata = xdata, ydata = ydata, maxfev = 10000000, p0 = (0,0,), bounds = [[0,0], [1,1]])
print(ParaOpt)    
Result = FitSIR(x, ParaOpt[0],ParaOpt[1])  
plt.plot(xdata,ydata, label='Actual')
plt.plot(xdata,Result, label='Fitted')
plt.xlabel('Time')
plt.title('Reported Cases')
plt.legend()
plt.savefig('Param_cal.png')

def sir_ode(times,init,parms):
    b, g = parms
    S,I,R = init
    # ODEs
    dS = -b*S*I
    dI = b*S*I-g*I
    dR = g*I
    return [dS,dI,dR]

parms = [4.94614556e-02, 9.22423666e-06]
init = [(1-0.107980-0.002039),0.107980,0.002039]
times = np.linspace(0,200,2001)

from scipy.integrate import ode, solve_ivp
sir_sol = solve_ivp(fun=lambda t, y: sir_ode(t, y, parms), t_span=[min(times),max(times)], y0=init, t_eval=times)

sir_out = pd.DataFrame({"t":sir_sol["t"],"S":sir_sol["y"][0],"I":sir_sol["y"][1],"R":sir_sol["y"][2]})

sline = plt.plot("t","S","",data=sir_out,color="red",linewidth=2)
iline = plt.plot("t","I","",data=sir_out,color="green",linewidth=2)
rline = plt.plot("t","R","",data=sir_out,color="blue",linewidth=2)
plt.xlabel("Time",fontweight="bold")
plt.ylabel("Number",fontweight="bold")
legend = plt.legend(title="Population",loc=5,bbox_to_anchor=(1.25,0.5))
frame = legend.get_frame()
frame.set_facecolor("white")
frame.set_linewidth(0)
plt.savefig('SIR_6.png')