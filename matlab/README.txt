Copyright (C) 2018 Intel Corporation
SPDX-License-Identifier: BSD-3-Clause

#########################
Welcome to the Intel WiFi RTT (FTM) 40MHz dataset.

The paper and the dataset can be downloaded from:
https://www.researchgate.net/publication/329887019_A_Machine_Learning_Approach_for_Wi-Fi_RTT_Ranging

To cite the dataset and code, or for further details, please use:
Nir Dvorecki, Ofer Bar-Shalom, Leor Banin, and Yuval Amizur, "A Machine Learning Approach for Wi-Fi RTT Ranging," ION Technical Meeting ITM/PTTI 2019

For questions/comments contact: 
nir.dvorecki@intel.com,
ofer.bar-shalom@intel.com, 
leor.banin@intel.com, 
yuval.amizur@intel.com

The zip file contains the following files:
1) This README.txt file.
2) LICENSE.txt file.
3) RTT_data.csv - the dataset of FTM transactions
4) Helper Matlab files:
	O mainFtmDatasetExample.m - main function to run in order to execute the Matlab example.
	O PlotFTMchannel.m - plots the channels of a single FTM transaction.
	O PlotFTMpositions.m - plots user and Access Point (AP) positions.
	O ReadFtmMeasFile.m - reads the RTT_data.csv file to numeric Matlab matrix.
	O SimpleFTMrangeEstimation.m - execute a simple range estimation on the entire dataset.
	O Office1_40MHz_VenueFile.mat - contains a map of the office from which the dataset was gathered.

#########################
Running the Matlab example:

In order to run the Matlab simulation, extract the contents of the zip file and call the mainFtmDatasetExample() function from Matlab.

#########################
Contents of the dataset:

The RTT_data.csv file contains a header row, followed by 29581 rows of FTM transactions.
The first column of the header row includes an extra "%" in the begining, so that the entire csv file can be easily loaded to Matlab using the command: load('RTT_data.csv')
Indexing the csv columns from 1 (leftmost column) to 467 (rightmost column):
O column 1 			- Timestamp of each measurement (sec)
O columns 2 to 4 	- Ground truth (GT) position of the client at the time the measurement was taken (meters, in local frame)
O column 5 			- Range, as estimated by the devices in real time (meters)
O columns 6 to 8 	- Access Point (AP) position (meters, in local frame)
O column 9 			- AP index/number, according the convention of the ION ITM 2019 paper
O column 10 		- Ground truth range between the AP and client (meters)
O column 11 		- Time of Departure (ToD) factor in meters, such that: TrueRange = (ToA_client + ToA_AP)*3e8/2 + ToD_factor (eq. 7 in the ION ITM paper, with "ToA" being tau_0 and the "ToD_factor" lumps up both nu initiator and nu responder)
O columns 12 to 467 - Complex channel estimates. Each channel contains 114 complex numbers denoting the frequency response of the channel at each WiFi tone:
						O columns 12 to 125  - Complex channel estimates for first antenna from the client device
						O columns 126 to 239 - Complex channel estimates for second antenna from the client device
						O columns 240 to 353 - Complex channel estimates for first antenna from the AP device
						O columns 354 to 467 - Complex channel estimates for second antenna from the AP device
					 The tone frequencies are given by: 312.5E3*[-58:-2, 2:58] Hz (e.g. column 12 of the csv contains the channel response at frequency fc-18.125MHz, where fc is the carrier wave frequency).
					 Note that the 3 tones around the baseband DC (i.e. around the frequency of the carrier wave), as well as the guard tones, are not included.
