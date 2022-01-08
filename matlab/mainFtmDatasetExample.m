% main - main function for simulation.
% usage: mainFtmDatasetExample(measFilePath, measIndex2Plot)

% This Matlab code is a supplement for the WiFi RTT (FTM) dataset.
% The dataset can be downloaded from:
% https://www.researchgate.net/publication/329887019_A_Machine_Learning_Approach_for_Wi-Fi_RTT_Ranging
% This code will read the CSV file containing the data and demonstrate how to process it in order to plot the WiFi channel and estimate ranges.
% 
% To cite the dataset and code, please use:
% Nir Dvorecki, Ofer Bar-Shalom, Leor Banin, and Yuval Amizur, "A Machine Learning Approach for Wi-Fi RTT Ranging," ION Technical Meeting ITM/PTTI 2019

% For questions/comments contact: 
% nir.dvorecki@intel.com,
% ofer.bar-shalom@intel.com, 
% leor.banin@intel.com, 
% yuval.amizur@intel.com

% Copyright (C) 2018 Intel Corporation
% SPDX-License-Identifier: BSD-3-Clause

function mainFtmDatasetExample(measFilePath, measIndex2Plot)
% This function will read the data CSV file. 
% It will then plot the frequency-domain channels and execute simple range estimation.
% Inputs: 
% measFilePath - full path of the provided RTT_data.csv file
% measIndex2Plot - an integer in the range [1,29581] that chooses which FTM transaction to plot.

% If user did not input the path of the measurement file, assume the code and data were extracted to the same folder.
% If user did not input an index of measurement to plot, choose one hardcoded.
if nargin == 1
    measIndex2Plot = 10;
elseif nargin == 0
    measIndex2Plot = 10;
    measFilePath = 'RTT_data.csv';
end

% Read the CSV file to get dataset as a matrix (measTable) along with a description for each column (tableIndexes)
[measTable,tableIndexes] = ReadFtmMeasFile(measFilePath);

% Extract client and AP positions and plot them in 2D
PlotFTMpositions(measTable, tableIndexes)

% Plot an example channel in the frequency domain
%PlotFTMchannel(measTable, tableIndexes, measIndex2Plot)

% Perform simple estimation for the range between APs and clients.
% Also plots the results as a CDF of the range errors.
%SimpleFTMrangeEstimation(measTable, tableIndexes)
end
