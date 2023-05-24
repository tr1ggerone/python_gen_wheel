# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:18:03 2023

@author: HuangAlan
"""
from self_module import main_func
import numpy as np
from sklearn import datasets

iris = datasets.load_iris()
data_iris = iris.data[50:,:]
label_iris = iris.target[50:,]
cr_iris = main_func.analysis_lda_loo(data_iris, label_iris, weight_p=1, weight_n=1)

data_time = np.load('test_data/time_series_data.npy')
bp_result = main_func.analysis_bp(data_time, 8, 12, 0, fs=500, bin_hz=10)

