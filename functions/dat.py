
def dat(rtt_data,sleep_time):
    print('Data science mode')

    import time
    import numpy as np
    import matplotlib.pyplot as plt
    
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
    # open figure
    plt.figure(figsize=(12,8))
    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.title('Access Point Positions X dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('X distance (meters) ')
    plt.savefig('graphs/X_positions_of_all_APs.jpg')

    # open figure
    plt.figure(figsize=(12,8))
    # Plot the AP Y positions for all access points
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.title('Access Point Positions Y dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Y distance (meters) ')
    plt.savefig('graphs/Y_positions_of_all_APs.jpg')

    # open figure
    plt.figure(figsize=(12,8))
    # Plot the AP X positions for all access points
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.savefig('graphs/Z_positions_of_all_APs.jpg')

    # open figure
    plt.figure(figsize=(12,8))
    # Plot all three dimensions on the same set of subplots

    plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions all dimensions')
    plt.xlabel('Access Point ID')
    plt.ylabel('Distance (meters)')
    plt.savefig('graphs/XYZ_plot_APs.jpg')

    # open figure
    plt.figure(figsize=(12,8))
    # 3D scatter plot 
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(rtt_data['AP_positionX[m]'], rtt_data['AP_positionY[m]'], rtt_data['AP_positionZ[m]'], color='g'); 
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    plt.savefig('graphs/3D_scatter_plot.jpg') 

