#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import winsound
import time
import subprocess
from timeit import default_timer as timer
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show , legend
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from sklearn import datasets, linear_model
import glob
import hashlib
m = hashlib.md5()
from PIL import Image
warnings.filterwarnings("ignore")
plt.close('all')
ts = time.time()
start = timer()
threshold= {
1:15000/3.6,
2:0,
3:10000/3.6,
4:250000/3.6,
5:700000/3.6,
6:5200
}
inputbins=30
#conversionlayer=input("Select the conversion layer:- [1 for Polyethylene], [2 for Lithium Floride], [3 for Boron Carbide] and [4 for no conversion layer]: ") 
cvalues= {
1:'PE',
2:'LiF',
3: 'B4C',
4: 'NCL',
}  
listlow=[]
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
m3rxthreshold=6
#pp = PdfPages('C:\Users\\bhesr928\Desktop\dataset\PixelPlotLinuxAll.pdf')
numberpartilces,angles,normalized=[],[],[]
datafiles = glob.glob("C:\Users\\bhesr928\Desktop\dataset\output_position_total*")
for key, value in cvalues.items():    
    for f in datafiles:
        X_parameters,Y_parameters=[],[]
        with open(f, 'rb') as infile:
            print f 
            finallist=[]
            positionnil= [[float(y) for y in x] for x in [x for x in map(lambda l: l.strip().split(','), infile.read().replace('(','').replace(')','').replace(' ','').split('\n')) if x != ['']]]
            countcurve,count,countblob,countline,countmultiple=0,0,0,0,0
            finallist= zip([x[0] for x in positionnil if x[4]>=threshold[m3rxthreshold]],[x[1] for x in positionnil if x[4]>=threshold[m3rxthreshold]],[x[2] for x in positionnil if x[4]>=threshold[m3rxthreshold]],[x[3] for x in positionnil if x[4]>=threshold[m3rxthreshold]])
            if (len(finallist)>0):
                primarynumber= finallist[0][0]
                print "Total number of particles: ",len(finallist)
                sortedlist= sorted([item[0] for item in positionnil], key=Counter([item[0] for item in positionnil]).get, reverse=True)
                d = {}
                for i in sortedlist: d[i] = d.has_key(i)
                nodubs= [k for k in d.keys() if not d[k]]   
                count=len(nodubs) 
                finallist1= [x for x in finallist if x[0] not in nodubs]
                countmultiple=len(finallist1)
                for i,j in zip(finallist1, finallist1[1:]):
                    count+=1
                    if i[0]==j[0]:
                        X_parameters.append(i[1])      
                        Y_parameters.append(i[2])
                    else:
                        #print X_parameters,Y_parameters
                        X_parameters.append(i[1])      
                        Y_parameters.append(i[2]) 
                        slope, intercept, r_value, p_value, std_err = stats.linregress(X_parameters, Y_parameters)  
                        X_parameters= [X_parameters[k:k+1] for k in range(0, len(X_parameters), 1)]
                        #plt.figure(figsize=(0.256, 0.256), dpi=100)  
                        fig = plt.figure(figsize=(3.31, 3.2), dpi=100)
                        ax = fig.add_subplot(111, axisbg='black')                 
                        if (r_value**2>0.75):
                                countline+=1
                        elif (r_value**2<0.75 and r_value**2>0.40):
                                countcurve+=1   
                        elif (r_value**2<0.75 and r_value**2!=0.0):
                                countblob+=1       
                        regr = linear_model.LinearRegression()  
                        regr.fit(X_parameters, Y_parameters)
                        #_image = np.zeros([256, 256], dtype=np.uint8)
                        plt.scatter(X_parameters,Y_parameters,facecolors='w', edgecolors='w',s=1)
                        #plt.show()
                        #_image[X_parameters, Y_parameters] = 255
                        #print _image
                        #_image = Image.fromarray(_image, 'L')
                        a=f.split(".")
                        #_image.save('C:\Users\\bhesr928\Desktop\outfolder'+str(i[0])+"_"+str(f.split("dataset\\")[1])+'.png')
                        #print f
                        plt.xlim(0,256)
                        plt.ylim(0,256)        
                        plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')         
                        ax.grid(False)
                        plt.savefig(str(i[0])+"_"+str(a[0].split("\\dataset\\")[1])+'.png',bbox_inches='tight',pad_inches = 0)
                        #pp.savefig()
                        #plt.plot(X_parameters,regr.predict(X_parameters),linewidth=4,label="R square value: "+str(r_value**2))
                        #plt.legend()
                        #plt.xlim(0,256)
                        #plt.ylim(0,256)                   
                        X_parameters, Y_parameters=[],[]      
                #print "\nNumber of multiple hits by single primary:",countmultiple
                #print "Straight line count with R square >0.75 is:", countline
                #print "Straight line count with R square <0.75 and >0.40 is:", countcurve
                #print "Straight line count with R square <0.45:", countblob
                #print "Number of single hits/photons: ",count
                        
winsound.Beep(2000, 100)
#p = subprocess.Popen([chrome_path,'C:\Users\\bhesr928\Desktop\dataset\PixelPlotLinuxAll.pdf'])
pp.close()
end = timer()
print "\nExecuted and plotted"
print 'Bin size choosen as: ', inputbins
print 'Total time elapsed', (end - start) / 60, 'mins.' 