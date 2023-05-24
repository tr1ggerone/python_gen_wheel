# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:00:06 2023

@author: HuangAlan
"""

# %%
def analysis_bp(data, band_start, band_end, ch_plot, fs=500, bin_hz=10):
    from .function_ref import function_BP
    
    bp_value = function_BP.BP(data, band_start, band_end, fs=fs)
    fig = function_BP.PSDplot(data, ch_plot, bin_hz=bin_hz, fs=fs)
    bp_result = dict(value=bp_value, pic=fig)
    
    return bp_result

# %%
def analysis_lda_loo(data, label, weight_p=1, weight_n=1):
    import numpy as np
    from .function_ref import function_LDA
    
    # ----- label transfer -----
    assert 1 in label
    label[label != 1] = 0
    
    # ----- lda loo -----
    loo_judge = []
    for i_tri in range(len(data)):
        data_tra = np.delete(data,i_tri,axis=0)
        label_tra = np.delete(label,i_tri,axis=0)
        data_tes = data[i_tri,:].reshape(1,-1)
        label_tes = label[i_tri,].reshape(1,)
        lda_result = function_LDA.LDA_test(data_tra, label_tra, 
                                           data_tes, label_tes, 
                                           weight_p=weight_p, weight_n=weight_n)
        loo_judge.append(lda_result['judge'])
    
    return sum(loo_judge)/len(data)
