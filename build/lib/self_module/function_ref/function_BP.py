# -*- coding: utf-8 -*-

__version__='0.1.0'
__author__ = 'Alan Huang'

# %%
def BP(data, band_start, band_end, fs=500):
    """
    **BP, Band Power is freqency-domain feature,need to set bandstart, bandEnd and sampling frequency**
    
    Args:
        data: ``array`` time series signal after feature extraction, size[numCh, numDp]
        bandStart: ``int/float`` start of frequency range (Hz)
        bandEnd: ``int/float`` end of frequency range  (Hz)
        fs: ``int/float`` sampling frequency (Hz), default as 500 Hz
    
    Returns
    -------
        value_bp:
            ``array``, return np.log(BP value) of data with input bandwidth, size[numCh,]
    """
    
    import numpy as np
    import numpy.fft as npfft
    
    # ----- initial parameter -----
    if data.ndim == 1:
        data = data.reshape(1, -1)
    [num_ch, num_dp] = data.shape
    num_time = num_dp/fs
    
    # ----- Fourier transform -----
    data_fft = npfft.fft(data, axis=1)
    data_psd = np.square(np.abs(data_fft))
    value_bp = np.sum(
        data_psd[:,int(np.round((band_start*num_time))):int(np.round((band_end*num_time)))], axis=1)
    
    return np.log(value_bp)

# %%
def PSDplot(data, ch_plot, bin_hz=10, fs=500):
    """
    **PSDplot, plot PSD and time series data in one figure**
    
    Args:
        data: ``array`` time series signal after feature extraction, size[numCh, numDp]
        ch_plot: ``int`` the channel user wants to show in figure
        bin_hz: ``int`` the unit of x-axis in psd plot, default as 10 Hz
        fs: ``int/float`` sampling frequency (Hz), default as 500 Hz
    
    Returns
    -------
        Figure
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    import numpy.fft as npfft
    
    # ----- initial parameter -----
    if data.ndim == 1:
        data = data.reshape(1, -1)
    [num_ch, num_dp] = data.shape
    
    # ----- Fourier transform -----
    data_fft = npfft.fft(data, axis=1)
    data_psd = np.square(np.abs(data_fft))
    plot_data = data[ch_plot,:]
    plot_data_psd = data_psd[ch_plot,:]
    
    # ----- psd plot -----
    FONT=12
    fig, ax = plt.subplots(2, 1, figsize=(18,6), dpi=80)
    ax[0].plot(plot_data, 'b', alpha=0.5, label='input data (time series)')
    ax[0].set_ylabel('Amplitude', fontsize=FONT)
    ax[0].set_xlabel('Sample Point', fontsize=FONT)
    ax[0].legend(loc='upper right')
    
    ax[1].plot(plot_data_psd[:int(len(plot_data_psd)/2)],
               'b', alpha=0.5, label='input data (PSD)')
    ax[1].set_ylabel('Power', fontsize=FONT)
    ax[1].set_xlabel('Hz', fontsize=FONT)
    ax[1].set_xticks(range(0, 
                           int(len(plot_data_psd)/2), 
                           int(bin_hz*len(plot_data_psd)/fs)))
    ax[1].set_ylim(0, max(plot_data_psd[1:]))
    ax[1].set_xticklabels(range(0, int(fs/2), bin_hz))
    ax[1].legend(loc='upper right')
    ax[1].grid(axis='x')
    
    return fig


    