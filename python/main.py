from ast import arg
from unicodedata import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def main():
    import argparse
    import sys
    import os
    from tabnanny import verbose

    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-path',
                        type=str,
                        help='the path to dataset')
    parser.add_argument('-m', 
                        '--mode',    
                        type=str,
                        help='c for communications engineering, d for data science mode')
    parser.add_argument("-v", 
                        "--verbose",    
                        type=int, 
                        help="increase output verbosity (1, 0)")

    # Parse arguments
    args = parser.parse_args()
    
    dataset_path = args.path
    mode=args.mode
    verbosity_level=args.verbose

    # Clean arguments

    if not os.path.isfile(dataset_path):
        print('The path specified does not exist')
        sys.exit() 

    # Execute main program 
    # Read the dataset into a pandas dataframe
    rtt_data = pd.read_csv(dataset_path) # Consider .xlsx input file format
    print('Data loaded ...\n') 
    sleep_time =3 

    time.sleep(sleep_time)

    if mode=='c' and not verbosity_level:
        comm(rtt_data, sleep_time)
        
    elif mode=='c' and verbosity_level:
        comm_v(rtt_data, sleep_time) 

    elif mode=='d' and not verbosity_level:
        dat(rtt_data, sleep_time)

    elif mode=='d' and verbosity_level:
        dat_v(rtt_data, sleep_time)

    else:
        default()
    

def comm(rtt_data, sleep_time):
    import matplotlib.pyplot as plt
    data=rtt_data
    print('Communications mode')
    # NB: The amplitude of the channels is usually not indicative of the SNR/RSSI. The channels were scaled by the hardware.
    freqz =312.5*1000 / 10**6   # MHz 
    tones =[freqz*i for i in range(-58,-1)] 
    tones2 = [freqz*i for i in range(2,59)]
    tone_frequencies = tones+tones2 # in MHz
    tone_frequencies=np.array(tone_frequencies) 
    # The "tone_frequencies" variable below is used to map which baseband frequency, in MHz, corresponds to each of the 114 tones.
    # Note that for 40MHz WiFi, the 3 tones around the DC are never observed

    measIndex2plot=22

    Channel_selection = data.iloc[measIndex2plot,12:468]
    Channel_selection= np.array(Channel_selection)
    ch_mean=Channel_selection[-1]
    Channel_selection=np.append(Channel_selection,ch_mean )
    example_channel_in_freq_domain =np.reshape(Channel_selection,[4,114]) 

    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

    dim1=0
    for index_ant in example_channel_in_freq_domain:
        dim2 = 0
        for val in index_ant:
            #example_channel_in_freq_domain[index_ant]
            fin_cplx_selection[dim1,dim2] = complex(val.replace('i', 'j'))
            dim2 +=1
        dim1+=1
    example_channel_in_freq_domain=np.array(fin_cplx_selection) 

    # Parameters for plot

    client_magnitude = np.abs(example_channel_in_freq_domain[0,])
    client_magnitude = np.array([20*np.log10(i) for i in client_magnitude])
    client_magnitude1= np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[1,]) ])


    ap_magnitude = np.abs(example_channel_in_freq_domain[2,])
    ap_magnitude = np.array([20*np.log10(i) for i in ap_magnitude])
    ap_magnitude1 = np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[3,])])

    client_phase = example_channel_in_freq_domain[0,]
    client_phase =np.array([np.angle(i) for i in client_phase])
    client_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[1,]])

    ap_phase = example_channel_in_freq_domain[2,]
    ap_phase =np.array([np.angle(i) for i in ap_phase])
    ap_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[3,]])

    # open figure
    plt.figure(figsize=(12,8))
    # Plot client side amplitude.
    plt.title('Example channel in frequency domain')
    plt.subplot(2,2,1)
    plt.plot(tone_frequencies, client_magnitude, tone_frequencies,client_magnitude1)
    plt.title('Channel amplitude at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')
    

    # plot AP side amplitude
    plt.subplot(2,2,2)
    plt.plot(tone_frequencies,ap_magnitude,tone_frequencies,ap_magnitude1) # 20*np.log10
    plt.title('Channel amplitude at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')

    # plot client side phase
    plt.subplot(2,2,3)
    plt.plot(tone_frequencies,client_phase,tone_frequencies,client_phase1)
    plt.title('Channel phase at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')

    # plot AP side phase
    plt.subplot(2,2,4)
    plt.plot(tone_frequencies,ap_phase,tone_frequencies,ap_phase1)
    plt.title('Channel phase at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')
    plt.show()

    dataset_columns = data.columns
    Channels_in_freq_domain = list(dataset_columns[12:467]) 

    freqz =312.5*1000 / 10**6   # MHz 
    tones =[freqz*i for i in range(-58,-1)] 
    tones2 = [freqz*i for i in range(2,59)]

    tone_frequencies = tones+tones2 # in MHz
    tone_frequencies=np.array(tone_frequencies)

    measIndex2plot =20
    Channel_selection = data.iloc[measIndex2plot,12:468]
    Channel_selection= np.array(Channel_selection)
    ch_mean=Channel_selection[-1]
    Channel_selection=np.append(Channel_selection,ch_mean )
    example_channel_in_freq_domain =np.reshape(Channel_selection,[4,114])

    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

    dim1=0
    for index_ant in example_channel_in_freq_domain:
        dim2 = 0
        for val in index_ant:
            #example_channel_in_freq_domain[index_ant]
            fin_cplx_selection[dim1,dim2] = complex(val.replace('i', 'j'))
            dim2 +=1
        dim1+=1
    example_channel_in_freq_domain=np.array(fin_cplx_selection)

    # Parameters for plot

    client_magnitude = np.abs(example_channel_in_freq_domain[0,])
    client_magnitude = np.array([20*np.log10(i) for i in client_magnitude])
    client_magnitude1= np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[1,]) ])

    ap_magnitude = np.abs(example_channel_in_freq_domain[2,])
    ap_magnitude = np.array([20*np.log10(i) for i in ap_magnitude])
    ap_magnitude1 = np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[3,])])

    client_phase = example_channel_in_freq_domain[0,]
    client_phase =np.array([np.angle(i) for i in client_phase])
    client_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[1,]])

    ap_phase = example_channel_in_freq_domain[2,]
    ap_phase =np.array([np.angle(i) for i in ap_phase])
    ap_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[3,]])

    # open figure
    plt.figure(figsize=(12,8))
    # Plot client side amplitude.
    plt.title('Example channel in frequency domain')
    plt.subplot(2,2,1)
    plt.plot(tone_frequencies, client_magnitude, tone_frequencies,client_magnitude1)
    plt.title('Channel amplitude at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')

    # plot AP side amplitude
    plt.subplot(2,2,2)
    plt.plot(tone_frequencies,ap_magnitude,tone_frequencies,ap_magnitude1) # 20*np.log10
    plt.title('Channel amplitude at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')


    # plot client side phase
    plt.subplot(2,2,3)
    plt.plot(tone_frequencies,client_phase,tone_frequencies,client_phase1)
    plt.title('Channel phase at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')

    # plot AP side phase
    plt.subplot(2,2,4)
    plt.plot(tone_frequencies,ap_phase,tone_frequencies,ap_phase1)
    plt.title('Channel phase at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')
    plt.show()


def comm_v(rtt_data, sleep_time):
    print('Verbose communications mode')
    
    import matplotlib.pyplot as plt
    data=rtt_data
    print('Communications mode')
    # NB: The amplitude of the channels is usually not indicative of the SNR/RSSI. The channels were scaled by the hardware.
    freqz =312.5*1000 / 10**6   # MHz 
    tones =[freqz*i for i in range(-58,-1)] 
    tones2 = [freqz*i for i in range(2,59)]
    tone_frequencies = tones+tones2 # in MHz
    tone_frequencies=np.array(tone_frequencies) 
    
    print('\nTone frequencies used: \n', tone_frequencies)
    time.sleep(sleep_time)
    # The "tone_frequencies" variable below is used to map which baseband frequency, in MHz, corresponds to each of the 114 tones.
    # Note that for 40MHz WiFi, the 3 tones around the DC are never observed

    measIndex2plot=22
    print('\nChosen index to plot: ',measIndex2plot)

    Channel_selection = data.iloc[measIndex2plot,12:468]
    Channel_selection= np.array(Channel_selection)
    ch_mean=Channel_selection[-1]
    Channel_selection=np.append(Channel_selection,ch_mean )
    example_channel_in_freq_domain =np.reshape(Channel_selection,[4,114]) 

    print('\nSelected channels to plot: ', example_channel_in_freq_domain)
    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

    dim1=0
    for index_ant in example_channel_in_freq_domain:
        dim2 = 0
        for val in index_ant:
            #example_channel_in_freq_domain[index_ant]
            fin_cplx_selection[dim1,dim2] = complex(val.replace('i', 'j'))
            dim2 +=1
        dim1+=1
    example_channel_in_freq_domain=np.array(fin_cplx_selection) 

    print('\nComplex channels selection: ', example_channel_in_freq_domain)
    # Parameters for plot

    client_magnitude = np.abs(example_channel_in_freq_domain[0,])
    client_magnitude = np.array([20*np.log10(i) for i in client_magnitude])
    client_magnitude1= np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[1,]) ])
    print('\nClient channels magnitudes: ', client_magnitude, client_magnitude1)

    ap_magnitude = np.abs(example_channel_in_freq_domain[2,])
    ap_magnitude = np.array([20*np.log10(i) for i in ap_magnitude])
    ap_magnitude1 = np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[3,])])
    print('\nAccess point magnitudes: ', ap_magnitude, ap_magnitude1)

    client_phase = example_channel_in_freq_domain[0,]
    client_phase =np.array([np.angle(i) for i in client_phase])
    client_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[1,]])
    print('\nClient phases: ', client_phase, client_phase1)


    ap_phase = example_channel_in_freq_domain[2,]
    ap_phase =np.array([np.angle(i) for i in ap_phase])
    ap_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[3,]])
    print('\nAP phases: ', ap_phase, ap_phase1)

    print('\n Drawing graphs for chosen example')
    # open figure
    plt.figure(figsize=(10,8))
    # Plot client side amplitude.
    plt.title('Example channel in frequency domain')
    plt.subplot(2,2,1)
    plt.plot(tone_frequencies, client_magnitude, tone_frequencies,client_magnitude1)
    plt.title('Channel amplitude at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')
    

    # plot AP side amplitude
    plt.subplot(2,2,2)
    plt.plot(tone_frequencies,ap_magnitude,tone_frequencies,ap_magnitude1) # 20*np.log10
    plt.title('Channel amplitude at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')

    # plot client side phase
    plt.subplot(2,2,3)
    plt.plot(tone_frequencies,client_phase,tone_frequencies,client_phase1)
    plt.title('Channel phase at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')

    # plot AP side phase
    plt.subplot(2,2,4)
    plt.plot(tone_frequencies,ap_phase,tone_frequencies,ap_phase1)
    plt.title('Channel phase at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')
    plt.show()

    dataset_columns = data.columns
    Channels_in_freq_domain = list(dataset_columns[12:467]) 

    freqz =312.5*1000 / 10**6   # MHz 
    tones =[freqz*i for i in range(-58,-1)] 
    tones2 = [freqz*i for i in range(2,59)]

    tone_frequencies = tones+tones2 # in MHz
    tone_frequencies=np.array(tone_frequencies)

    measIndex2plot =20
    Channel_selection = data.iloc[measIndex2plot,12:468]
    Channel_selection= np.array(Channel_selection)
    ch_mean=Channel_selection[-1]
    Channel_selection=np.append(Channel_selection,ch_mean )
    example_channel_in_freq_domain =np.reshape(Channel_selection,[4,114])

    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

    dim1=0
    for index_ant in example_channel_in_freq_domain:
        dim2 = 0
        for val in index_ant:
            #example_channel_in_freq_domain[index_ant]
            fin_cplx_selection[dim1,dim2] = complex(val.replace('i', 'j'))
            dim2 +=1
        dim1+=1
    example_channel_in_freq_domain=np.array(fin_cplx_selection)

    # Parameters for plot

    client_magnitude = np.abs(example_channel_in_freq_domain[0,])
    client_magnitude = np.array([20*np.log10(i) for i in client_magnitude])
    client_magnitude1= np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[1,]) ])

    ap_magnitude = np.abs(example_channel_in_freq_domain[2,])
    ap_magnitude = np.array([20*np.log10(i) for i in ap_magnitude])
    ap_magnitude1 = np.array([20*np.log10(i) for i in np.abs(example_channel_in_freq_domain[3,])])

    client_phase = example_channel_in_freq_domain[0,]
    client_phase =np.array([np.angle(i) for i in client_phase])
    client_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[1,]])

    ap_phase = example_channel_in_freq_domain[2,]
    ap_phase =np.array([np.angle(i) for i in ap_phase])
    ap_phase1 =np.array([np.angle(i) for i in example_channel_in_freq_domain[3,]])

    print('\n Drawing graphs for mean dataset')

    # open figure
    plt.figure(figsize=(10,8))
    # Plot client side amplitude.
    plt.title('Example channel in frequency domain')
    plt.subplot(2,2,1)
    plt.plot(tone_frequencies, client_magnitude, tone_frequencies,client_magnitude1)
    plt.title('Channel amplitude at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')

    # plot AP side amplitude
    plt.subplot(2,2,2)
    plt.plot(tone_frequencies,ap_magnitude,tone_frequencies,ap_magnitude1) # 20*np.log10
    plt.title('Channel amplitude at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Amplitude[dB]')


    # plot client side phase
    plt.subplot(2,2,3)
    plt.plot(tone_frequencies,client_phase,tone_frequencies,client_phase1)
    plt.title('Channel phase at client side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')

    # plot AP side phase
    plt.subplot(2,2,4)
    plt.plot(tone_frequencies,ap_phase,tone_frequencies,ap_phase1)
    plt.title('Channel phase at AP side')
    plt.xlabel('Tone frequency[MHz]')
    plt.ylabel('Phase[rad]')
    plt.show()

def dat(rtt_data,sleep_time):
    print('Data science mode')

    # Print the entire data 
    print('\nWhole dataset:\n')
    print(rtt_data) 
    time.sleep(sleep_time)

    # Dataset head
    print('\nDataset head:\n')
    print(rtt_data.head())  # Consider that head takes one parameter
    time.sleep(sleep_time)

    # Dataset tail
    print('\nDataset tail:\n')
    print(rtt_data.tail()) # Consider that tail takes one parameter
    time.sleep(sleep_time)

    # Dataset shape
    print('\nDataset shape:\n')
    print(rtt_data.shape)
    time.sleep(sleep_time)

    # Number of observations
    print('\nNumber of observations:\n')
    print(rtt_data.shape[0])
    time.sleep(sleep_time)

    # Number of columns
    print('\nNumber of columns:\n')
    print(rtt_data.shape[1])
    time.sleep(sleep_time)

    # What are the columns in the data
    print('\nData columns:\n',[col for col in rtt_data.columns])
    time.sleep(sleep_time)

    # Read a selected column
    print('\nSelected Column:\n',rtt_data['GroundTruthPositionX[m]']) # Consider index slicing inside the column, 
    time.sleep(sleep_time)
    # list of column names
    print('\nSelected Columns:\n',rtt_data[['GroundTruthPositionX[m]', 'GroundTruthPositionY[m]', 'GroundTruthPositionZ[m]']]) # Consider index slicing inside the column, 
    time.sleep(sleep_time)
    # Read a selected row 
    print('\nSelected Row:\n',rtt_data.iloc[1])
    time.sleep(sleep_time)

    # Read a range of rows
    print('\nSelected Rows:\n',rtt_data.iloc[1:4])
    time.sleep(sleep_time)

    # Read specific data point described by row and column
    print('\nSpecific datum:\n',rtt_data.iloc[2,3])
    time.sleep(sleep_time)

    # Describe the data
    rtt_data.describe() 
    time.sleep(sleep_time)

    # Plot the AP X positions for all access points
    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.title('Access Point Positions X dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('X distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    # Plot the AP X positions for all access points
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.title('Access Point Positions Y dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Y distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    # Plot the AP X positions for all access points
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    # Plot all three dimensions on the same set of subplots
    plt.figure(figsize=(15, 3))
    plt.subplot(131)
    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.title('Access Point Positions X dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('X distance (meters) ')
    plt.subplot(132)
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.title('Access Point Positions Y dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Y distance (meters) ')
    time.sleep(sleep_time)
    plt.close()


    plt.subplot(133)
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()


    # Plot all three dimensions on the same set of subplots

    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions all dimensions')
    plt.xlabel('Access Point ID')
    plt.ylabel('Distance (meters)')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    # 3D scatter plot 
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(rtt_data['AP_positionX[m]'], rtt_data['AP_positionY[m]'], rtt_data['AP_positionZ[m]'], color='g'); 
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    plt.show()
    time.sleep(sleep_time)
    plt.close()


def dat_v(rtt_data,sleep_time):
    print('Verbose data science mode')
    time.sleep(sleep_time)
    # Print the entire data 
    print('\n Print out the whole dataset:\n')
    print(rtt_data) 
    time.sleep(sleep_time)

    # Dataset head
    print('\nDataset head: (first five rows of the dataset) \n')
    print(rtt_data.head())  # Consider that head takes one parameter
    time.sleep(sleep_time)

    # Dataset tail
    print('\nDataset tail: (last five rows of the dataset)\n')
    print(rtt_data.tail()) # Consider that tail takes one parameter
    time.sleep(sleep_time)

    # Dataset shape
    print('\nDataset shape: (number of rows and columns)\n')
    print(rtt_data.shape)
    time.sleep(sleep_time)

    # Number of observations
    print('\nNumber of observations: (number of rows) \n')
    print(rtt_data.shape[0])
    time.sleep(sleep_time)

    # Number of columns
    print('\nNumber of columns: (observed attributes) \n')
    print(rtt_data.shape[1])
    time.sleep(sleep_time)

    # What are the columns in the data
    print('\nData columns: (column names for all columns) \n',[col for col in rtt_data.columns])
    time.sleep(sleep_time)

    # Read a selected column
    print('\nSelected Column: (random selection) \n',rtt_data['GroundTruthPositionX[m]']) # Consider index slicing inside the column, 
    time.sleep(sleep_time)
    
    # list of column names
    print('\nSelected Columns: (multiple columns ) \n',rtt_data[['GroundTruthPositionX[m]', 'GroundTruthPositionY[m]', 'GroundTruthPositionZ[m]']]) # Consider index slicing inside the column, 
    time.sleep(sleep_time)
    # Read a selected row 
    print('\nSelected Row: (random selection) \n',rtt_data.iloc[1])
    time.sleep(sleep_time)

    # Read a range of rows
    print('\nSelected Rows: (multiple rows) \n',rtt_data.iloc[1:4])
    time.sleep(sleep_time)

    # Read specific data point described by row and column
    print('\nSpecific datum: (random datum-row, column value) \n',rtt_data.iloc[2,3])
    time.sleep(sleep_time)

    # Describe the data
    print('Main statistical properties of the data')
    rtt_data.describe() 
    time.sleep(sleep_time)


    print('Plot the AP X positions for all access points')
    # Plot the AP X positions for all access points
    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.title('Access Point Positions X dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('X distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close('all')

    print('Plot the AP Y positions for all access points')
    # Plot the AP Y positions for all access points
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.title('Access Point Positions Y dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Y distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    print('Plot the AP Z positions for all access points')

    # Plot the AP Z positions for all access points
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    print('Plot all three dimensions on the same set of subplots')
    # Plot all three dimensions on the same set of subplots
    plt.figure(figsize=(15, 3))
    plt.subplot(131)
    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.title('Access Point Positions X dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('X distance (meters) ')
    plt.subplot(132)
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.title('Access Point Positions Y dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Y distance (meters) ')
    time.sleep(sleep_time)
    plt.close()


    plt.subplot(133)
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.show()
    time.sleep(sleep_time)
    plt.close()


    # Plot all three dimensions on the same set of subplots
    print('Plot all three dimensions on the same set of subplots')
    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions all dimensions')
    plt.xlabel('Access Point ID')
    plt.ylabel('Distance (meters)')
    plt.show()
    time.sleep(sleep_time)
    plt.close()

    print('3D scatter plot')
    # 3D scatter plot 
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(rtt_data['AP_positionX[m]'], rtt_data['AP_positionY[m]'], rtt_data['AP_positionZ[m]'], color='g'); 
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    plt.show()
    time.sleep(sleep_time)
    plt.close()


def default():
    print('Combined mode')

if __name__ =="__main__":
    main()




