# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:48:26 2018

@author: OhWhee
"""

import numpy as np

#w = 20
#for i in xrange(100):
#    w = w -0.1*2*w

w = 3
for i in range(1000):
    w = w-0.01*((2*w)+(4*np.power(w, 3)))
    print(w)
