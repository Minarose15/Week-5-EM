# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:50:57 2021

@author: Sabrina
"""

from numpy import pi, zeros, max, copy, gradient, linspace, meshgrid, transpose
from pylab import imshow, plasma, show, quiver, axes


class Capacitor:
    
    def __init__(self, d, L):
        self.d = d
        self.L = L
        self.Voltage = zeros([self.L,self.L], float)
        self.Voltage[int(self.L/2-self.L/6):int(self.L+self.L/6)+1, 
                     int(self.L-self.d*self.L/4)] = 1
        self.Voltage[int(L/2-L/6):int(L/2+L/6)+1, int(L/2+self.d*L/4)]= -1
        
    def SOR(self):
            delta = 2.0e-4
            size = self.Voltage.shape
            alpha = 2/(1+pi/size[0])
            while(delta > 1.0e-8):
                VOld_emort = copy(self.Voltage)
                for i in range(1, size[0]-1):
                    for j in range(1, size[1]-1):
                        if (i < int(self.L/2-self.L/6) or 
                            i > int(self.L/2+self.L/6) or
                            (j != int(self.L/2-self.d*self.L/4) and 
                             j != int(self.L/2+self.d*self.L/4))):
                            self.Voltage[i][j] = 0.25*(self.Voltage[i+1][j]+
                                                       self.Voltage[i-1][j]+
                                                       self.Voltage[i][j+1]+
                                                       self.Voltage[i][j-1])
                            deltaV = self.Voltage[i][j] - VOld_emort[i][j]
                            self.Voltage[i][j] = alpha * deltaV + VOld_emort[i][j]
                delta = max(abs(self.Voltage-VOld_emort))
            
    def voltagePlot(self):
        self.SOR()
        imshow(self.Voltage)
        plasma()
        show()
        
    def ElectricField(self):
        return gradient(self.Voltage)
    
    def electricPlot(self):
        self.SOR()

        x = linspace(0,self.L,self.L)        #makes ranges to loop through, 150 points in each
        y = linspace(0,self.L,self.L)
        X,Y = meshgrid(x,y)
        dX, dY = gradient(transpose(self.Voltage)0)
        quiver(X, Y, dX, dY, color = "k")
        axes().set_aspect('equal')
        show()

capac8 = Capacitor(0.8,50)
#capac8.voltagePlot()

capac3 = Capacitor(0.3,50)
#capac3.voltagePlot()

capac10 = Capacitor(1.0, 50)
capac8.electricPlot()
capac3.electricPlot()
capac10.electricPlot()