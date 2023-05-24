# -*- coding: utf-8 -*-

__version__='0.1.0'
__author__ = 'Alan Huang'

# %%
def LDA_test(data_tra, label_tra, data_tes, label_tes, weight_p=1, weight_n=1):
    """
    **LDA_test, use data_tra to bulid a LDA model and output the result of data_tes, data need to be 2-class**
    
    Args:
        data_tra: ``array`` time series signal after feature extraction, size[numTrial(samples), numFeature]
        label_tra: ``array`` the label of dataTrain, same length with dataTrain, size[numTrial, 1]
        data_tes: ``array`` time series signal after feature extraction, size[numTrial(samples), numFeature]
        label_tes: ``array`` the label of dataTest, same length with dataTest, size[numTrial, 1]
        c: ``float`` present the penalty weight of weight_p and weight_n, default as 1
        
    Returns
    -------
        Result:
            ``list`` [Cr,BL,Tpr,Tnr]
            ::
                Cr {float}: classification rate
                BL {float}: Balance Loss
                Tpr {float}: true positive rate, sensitivity
                Tnr {float}: true negative rate, specificity
        Decision:
            ``2-D array`` return the result of dataTest, same length with dataTest, size[numTrial, 1]
    """
    import numpy as np
    
    # ----- shape data -----
    [num_trial, num_fea] = np.shape(data_tra)
    num_tes = np.shape(data_tes)[0]
    
    # ----- resort data_tra -----
    c_p = np.sum(label_tra == 1)
    c_n = np.sum(label_tra != 1)
    data_tra_p = data_tra[np.where(label_tra == 1)[0],:]
    data_tra_n = data_tra[np.where(label_tra != 1)[0],:]
    
    # ----- average value of each class -----
    u_p = np.mean(data_tra_p,axis=0).reshape(-1,1)
    u_n = np.mean(data_tra_n,axis=0).reshape(-1,1)
    
    # ----- prior probability of each class -----
    pi_p = c_p/(c_p+c_n)
    pi_n = c_n/(c_p+c_n)
    
    # ----- covariance matrix -----
    sigma_p = np.cov(data_tra_p.T, bias=True)
    sigma_n = np.cov(data_tra_n.T, bias=True)
    sigma_class = pi_p*sigma_p+pi_n*sigma_n
    
    # ----- Checking Singilar matrix -----
    if type(sigma_class) is np.float64: 
        sigma_class = sigma_class.reshape(1,1)
    try:
        tmp_D = np.transpose(u_p-u_n)@np.linalg.pinv(sigma_class, rcond=1e-15, 
                                                      hermitian=False)
    except np.linalg.LinAlgError as err:
        if 'SVD did not converge' in str(err):
            tmp_D = np.transpose(u_p-u_n)@np.linalg.pinv(sigma_class, 
                                                         rcond=1e-15, 
                                                         hermitian=True)
        else:
            tmp_D = np.transpose(u_p-u_n)@np.linalg.pinv(sigma_class+1e-10,
                                                         rcond=1e-15, 
                                                         hermitian=True)

    # ----- Decision function -----
    dec = []
    _tp = 0
    _fp = 0
    _tn = 0
    _fn = 0
    for i_tri in range(num_tes):
        _d = tmp_D@data_tes[i_tri,:]-0.5*tmp_D@(u_p+u_n)-np.log((weight_n*pi_n)/(weight_p*pi_p))
        dec.append(_d[0,0])

        if label_tes[i_tri] == 1:
            if np.sign(_d) == 1:
                _tp+=1
            else:
                _fn+=1
        if label_tes[i_tri] != 1:
            if np.sign(_d) == -1:
                _tn+=1
            else:
                _fp+=1
    
    # ----- retrun result -----
    try:
        lda_result = {}
        lda_result['CR'] = (_tp+_tn)/(_tp+_tn+_fp+_fn)
        lda_result['TPR'] = _tp/(_tp+_fn)
        lda_result['TNR'] = _tn/(_tn+_fp)
        lda_result['BL'] = (lda_result['TPR']+lda_result['TNR'])/2
    except:
        lda_result = dict(CR=(_tp+_tn)/(_tp+_tn+_fp+_fn))
    label_jdg = np.sign(dec)
    label_jdg[np.where(label_jdg == -1)] = 0
    lda_result['judge'] = (label_jdg == label_tes)

    return lda_result

    