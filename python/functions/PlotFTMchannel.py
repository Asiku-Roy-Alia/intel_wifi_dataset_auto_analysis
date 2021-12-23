# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import matplotlib.pyplot as plt
    
def PlotFTMchannel(measTable = None,ind = None,measIndex2Plot = None): 
    # This function plots an example channel in the frequency domain
    # Inputs:
    # measTable - a numeric 2D metrix in which each row is an FTM transaction and each column is a variable
    # ind - a struct containing fields APpos and GTpos that indicate which columns in measTable contain the AP positions and ground truth positions,
    #       respectively
    # measIndex2Plot - an integer in the range [1,29581] (size of the dataset) that chooses which FTM transaction to plot.
        
    Channels_in_freq_domain = measTable(ind.channels)
    
    # NOTE: The amplitude of the channels is usually not indicative of the SNR/RSSI. The channels were scaled by the hardware.
    
    # The "tone_frequencies" variable below is used to map which baseband frequency, in MHz, corresponds to each of the 114 tones.
    # Note that for 40MHz WiFi, the 3 tones around the DC are never observed
    Channels_in_freq_domain = measTable(ind.channels)
    
    
    # reshape the chosen example channel such that the first dimension is the tone
    # index, the second is the antenna and the third is the device (client is "side 1", AP is "side 2")
    example_channel_in_freq_domain = np.reshape(Channels_in_freq_domain(measIndex2Plot,:), tuple(np.array([114,2,2])), order="F")
    # open figure
    figure
    plt.title('Example channel in frequency domain')
    # plot client side amplitude.
    subplot(2,2,1)
    plt.plot(tone_frequencies,20 * log10(np.abs(example_channel_in_freq_domain(:,:,1))))
    plt.title('Channel amplitude at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')
    # plot AP side amplitude
    subplot(2,2,2)
    plt.plot(tone_frequencies,20 * log10(np.abs(example_channel_in_freq_domain(:,:,2))))
    plt.title('Channel amplitude at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')
    # plot client side phase
    subplot(2,2,3)
    plt.plot(tone_frequencies,angle(example_channel_in_freq_domain(:,:,1)))
    plt.title('Channel phase at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')
    # plot AP side phase
    subplot(2,2,4)
    plt.plot(tone_frequencies,angle(example_channel_in_freq_domain(:,:,2)))
    plt.title('Channel phase at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')
    return
    