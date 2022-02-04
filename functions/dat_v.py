
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
    #time.sleep(sleep_time)
    plt.close('all')

    print('Plot the AP Y positions for all access points')
    # Plot the AP Y positions for all access points
    plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
    plt.title('Access Point Positions Y dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Y distance (meters) ')
    plt.show()
    #time.sleep(sleep_time)
    plt.close()

    print('Plot the AP Z positions for all access points')

    # Plot the AP Z positions for all access points
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.show()
    #time.sleep(sleep_time)
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
    #time.sleep(sleep_time)
    plt.close()


    plt.subplot(133)
    plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
    plt.title('Access Point Positions Z dimension')
    plt.xlabel('Access Point ID') 
    plt.ylabel('Z distance (meters) ')
    plt.show()
    #time.sleep(sleep_time)
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
    #time.sleep(sleep_time)
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
    #time.sleep(sleep_time)
    plt.close()
