def estimate_range(selected_row_in, RTT_data):
    import matplotlib.pyplot as plt 
    import numpy as np

    # We do range estimation for just one observation received as an argument
    selected_row = selected_row_in
    selected_data = RTT_data.iloc[selected_row] # Select row from dataset

    channels_begin = 11 # Channels start at column 11
    channel_batch_size =114 # Each antenna has 114 complex channel estimates

    channels_unpadded = selected_data[channels_begin:channels_begin+2*channel_batch_size]   # Select all channels for antenna 1

    np_channels = np.array(channels_unpadded) # Convert to numpy array 

    np_channels_cplx = np.zeros_like(np_channels) # Initialize a same-shape array 

    # Convert channels from string to complex
    counter = 0
    for ch_rsp in np_channels:
        ch_rsp= complex(ch_rsp.replace('i', 'j')) 
        np_channels_cplx[counter] = ch_rsp 
        counter+=1

    # Assign the complex channels to a new variable 

    channels_unpadded_raw = np_channels_cplx 

    # Add DC tones and guard subcarriers for 40MHz Wi-Fi
    sub_channel_batch_size = 57

    zeros_to_pad = 28 
    channels = np.zeros(2*channel_batch_size+28, dtype=complex)
    current_index = 6 
    channels[current_index:sub_channel_batch_size+current_index] = channels_unpadded_raw[:sub_channel_batch_size]
    current_index += (sub_channel_batch_size +3)
    channels[current_index:current_index+sub_channel_batch_size] = channels_unpadded_raw[sub_channel_batch_size:channel_batch_size]
    current_index += (sub_channel_batch_size+11)
    channels[current_index:current_index+sub_channel_batch_size] = channels_unpadded_raw[channel_batch_size:sub_channel_batch_size+channel_batch_size] 
    current_index += (sub_channel_batch_size+3)
    channels[current_index:current_index+sub_channel_batch_size] =  channels_unpadded_raw[sub_channel_batch_size+channel_batch_size:2*channel_batch_size]
    channels.shape

    # Client, AP channels
    channels_client = channels[:128]
    channels_ap = channels[128:] 

    # Convert to time domain using the inverse fast fourier transform 
    channels_timedomain = np.fft.ifft(np.fft.ifftshift(channels_client))
    channels_timedomain_ap = np.fft.ifft(np.fft.ifftshift(channels_ap))

    N_samples_to_shift = 13; # integer number of samples to circular shift
    channel_time_domain_circ_shifted = np.roll(channels_timedomain, N_samples_to_shift)
    channel_time_domain_circ_shifted_ap = np.roll(channels_timedomain_ap, N_samples_to_shift)


    if selected_row_in==2:
        plt.plot(channels_timedomain.real, label='real')
        plt.plot(channels_timedomain.imag, '--',  label='imaginary')
        plt.title('Client') 
        plt.legend()
        plt.show()

        plt.plot(channels_timedomain_ap.real, label='real')
        plt.plot(channels_timedomain_ap.imag, '--',  label='imaginary') 
        plt.title('Access point')
        plt.legend()
        plt.show()

        
        plt.plot(np.abs(channels_timedomain))
        plt.xlabel('Time index')
        plt.ylabel('Channel Magnitude')
        plt.title('Channel magnitudes')
     

        plt.plot(channel_time_domain_circ_shifted.real, label='real')
        plt.plot(channel_time_domain_circ_shifted.imag, '--',  label='imaginary') 
        plt.title('Channels circular shifted')
        plt.legend()
        plt.show()

        plt.plot(channel_time_domain_circ_shifted_ap.real, label='real')
        plt.plot(channel_time_domain_circ_shifted_ap.imag, '--',  label='imaginary') 
        plt.title('AP channels circular shifted')
        plt.legend()
        plt.show()
    

    est_ToA_index_client = np.argmax(channel_time_domain_circ_shifted)

    est_ToA_index_AP = np.argmax(channel_time_domain_circ_shifted_ap)
    
    # Correct ToA indexes by -N_samples_to_shift
    est_ToA_index_client    = est_ToA_index_client - N_samples_to_shift
    est_ToA_index_AP        = est_ToA_index_AP - N_samples_to_shift

    # Translate the sample index to time in seconds
    # The channels are sampled at 40MHz. The entire symbol is 3.2usec length.
    delta_time_per_sample = 1/40e6 # time difference between each two samples (sec)
    est_ToA_client = (est_ToA_index_client - 1)*delta_time_per_sample  # estimated client ToA in seconds
    est_ToA_AP     = (est_ToA_index_AP - 1)*delta_time_per_sample      # estimated AP ToA in seconds

    print('Client ToA estimate:',est_ToA_client,'AP ToA estimate: ', est_ToA_AP)

    # Calculate estimated range and range error
    ToD_factor = selected_data['ToD_factor[m]'] # in meters RTT_data(:,ind.ToDfactor)
    est_range = ToD_factor + (est_ToA_client + est_ToA_AP)*3e8/2 # estimated range [m]
    GT_range = selected_data['GroundTruthRange[m]'] # ground truth range for this measurement [m]
    ml_range_estimate = selected_data['ML_range_estimate[m]']
    range_error = est_range - GT_range # estimated range error [m] 
    print('ToD factor',ToD_factor,'estimated range',est_range,'Ground truth range', GT_range, 'range error', range_error,'n','ML range estimate',ml_range_estimate)

    return est_range, GT_range,ml_range_estimate
