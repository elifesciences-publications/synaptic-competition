# Plotting CV from multiple simulations

# This program was used to create Fig. 8C,D of the manuscript.
# It plots the CV of w_i of 7 synapses from multiple simulations and combines them into one figure.
# To get the data for the CV please run stochasticSimulation.py

import numpy as np
from  matplotlib import pyplot as plt
from scipy import stats,polyval, polyfit, linspace

##################################################
###### extract the data from the text files ######
##################################################

cv = []

for i in range(1,4):
    cv_i = np.array([])
    # please name the files with CV data differently, like cv1, cv2, ...
    data_text = "cv"+str(i) 
    data = open(data_text) 
    
    counter = 0
    for line in data:
        if counter == 7:
            break
        cv_i = np.append(cv_i, float(line.rstrip())) 
        counter += 1
        
    data.close()
    cv.append(cv_i)

##################################################
################# regression #####################
##################################################
    
regression = []
x_axis_cv = []
F = [0.5,0.7,0.9] # set F here for scaling the x axis (F*s_i)
x_axis_regression = np.linspace(0.0,120,500,endpoint=True)

for i in range(1,4):
    x_axis_i = np.array([1,2,5,10,20,50,100])*F[i-1]
    av_x_axis_i = sum(np.log(x_axis_i))/len(x_axis_i)
    av_cv_i = sum(np.log(cv[i-1]))/len(cv[i-1])

    b_cv_i = sum((np.log(x_axis_i)-av_x_axis_i)*\
      (np.log(cv_i)-av_cv_i))/sum((np.log(x_axis_i)-av_x_axis_i)**2)
    a_cv_i = av_cv_i-b_cv_i*av_x_axis_i
    
    regression.append(np.exp(a_cv_i)*(x_axis_regression**b_cv_i))
    x_axis_cv.append(x_axis_i)
    
##################################################
#################### plot ########################
##################################################
    
f = plt.figure(figsize=(4,3))
font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 12}
plt.rc('font', **font)
plt.rc('font', serif='Times New Roman') 
plt.rc('text', usetex=True)

plt.xscale('log')
plt.yscale('log')
colors = ['green','cyan','darkviolet']
labels = [r'$\phi=1.0$', r'$\phi=2.67$',r'$\phi=5.0$']

for i in range(3):
    plt.plot(x_axis_cv[i], cv[i],'.',color=colors[i],label=labels[i])
    plt.plot\
      (x_axis_regression, regression[i],'-',color=colors[i],alpha = 0.3)

plt.ylabel(r'$CV \; [{\rm \%}]$', fontsize=12)
plt.xlabel(r'$Fs_i$', fontsize=12)
plt.legend(loc=1, fontsize=12)
plt.show()
# set the name of the file here
f.savefig("plot_cv_FigCD.pdf", bbox_inches='tight')
