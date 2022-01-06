# Import required modules 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt  
import functions
from functions.ReadFtmMeasFile import ReadFtmMeasFile

# Import dataset 
dataset_path =r'E:\work\masters\Trento\Academics\Semesters\Year 1 Semester 1\146069 Next Generation Networks\project\execution\data\Data\RTT_data.csv' 

# *****************************************************************************
# *****************************************************************************
#  Pure data science perspective of the data     ******************************
#                                                                             *
# *****************************************************************************

# Read the dataset into a pandas dataframe
rtt_data = pd.read_csv(dataset_path) # Consider .xlsx input file format
print('Data loaded ...\n')

# Print the entire data 
print('\nWhole dataset:\n')
print(rtt_data) 

# Dataset head
print('\nDataset head:\n')
print(rtt_data.head())  # Consider that head takes one parameter

# Dataset tail
print('\nDataset tail:\n')
print(rtt_data.tail()) # Consider that tail takes one parameter

# Dataset shape
print('\nDataset shape:\n')
print(rtt_data.shape)

# Number of observations
print('\nNumber of observations:\n')
print(rtt_data.shape[0])

# Number of columns
print('\nNumber of columns:\n')
print(rtt_data.shape[1])

# What are the columns in the data
print('\nData columns:\n',[col for col in rtt_data.columns])

# Read a selected column
print('\nSelected Column:\n',rtt_data['GroundTruthPositionX[m]']) # Consider index slicing inside the column, 
# list of column names
print('\nSelected Columns:\n',rtt_data[['GroundTruthPositionX[m]', 'GroundTruthPositionY[m]', 'GroundTruthPositionZ[m]']]) # Consider index slicing inside the column, 

# Read a selected row 
print('\nSelected Row:\n',rtt_data.iloc[1])

# Read a range of rows
print('\nSelected Rows:\n',rtt_data.iloc[1:4])

# Read specific data point described by row and column
print('\nSpecific datum:\n',rtt_data.iloc[2,3])

# Iterate through values
#for index, row in rtt_data.iterrows():
#    print(index,row)

# df.loc attribute 


# Describe the data
rtt_data.describe() 

# rtt_data.sort() 

# rtt_data filter operations

# Plot the AP X positions for all access points
plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
plt.title('Access Point Positions X dimension')
plt.xlabel('Access Point ID') 
plt.ylabel('X distance (meters) ')
plt.show()


# Plot the AP X positions for all access points
plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
plt.title('Access Point Positions Y dimension')
plt.xlabel('Access Point ID') 
plt.ylabel('Y distance (meters) ')
plt.show()

# Plot the AP X positions for all access points
plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
plt.title('Access Point Positions Z dimension')
plt.xlabel('Access Point ID') 
plt.ylabel('Z distance (meters) ')
plt.show()

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

plt.subplot(133)
plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
plt.title('Access Point Positions Z dimension')
plt.xlabel('Access Point ID') 
plt.ylabel('Z distance (meters) ')
plt.show()

# Plot all three dimensions on the same set of subplots

plt.plot(rtt_data['AP_positionX[m]'], color='green', marker ='o')
plt.plot(rtt_data['AP_positionY[m]'],marker ='o') 
plt.plot(rtt_data['AP_positionZ[m]'],color='red', marker ='o')
plt.title('Access Point Positions all dimensions')
plt.xlabel('Access Point ID')
plt.ylabel('Distance (meters)')
plt.show()

# 3D scatter plot 
from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(rtt_data['AP_positionX[m]'], rtt_data['AP_positionY[m]'], rtt_data['AP_positionZ[m]'], color='g'); 
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.show()

# *****************************************************************************
# *****************************************************************************
#  Communications theory perspective of the data     **************************
#                                                                             *
# *****************************************************************************

