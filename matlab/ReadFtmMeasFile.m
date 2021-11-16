% Copyright (C) 2018 Intel Corporation
% SPDX-License-Identifier: BSD-3-Clause

function [data, ind] = ReadFtmMeasFile(measFilePath)
% This function will read the data CSV file. 
% Inputs: 
% measFilePath - full path of the provided RTT_data.csv file
% Outputs:
% data - numeric matrix containing the entire dataset
% ind - a utility struct with the indexes of each type of data in the output matrix "data"

%% Read CSV file as matrix
data = csvread(measFilePath,1,0);

%% Indexes of each type of data in the CSV matrix
ind.timestamp = 1;          % Timestamp of each measurement (sec)
ind.GTpos = [2:4];          % Ground truth (GT) position of the client (meters, in local frame)
ind.ML_est_range = 5;       % Range estimated by the devices in real time (meters)
ind.APpos = [6:8];          % Access Point (AP) position (meters, in local frame)
ind.APnum = 9;              % AP index/number, according the convention of the ION ITM 2019 paper
ind.GTrange = 10;           % Ground truth range between the AP and client (meters)
ind.ToDfactor = 11;         % Time of Departure (ToD) factor in meters, such that: TrueRange = (ToA_client + ToA_AP)*3e8/2 + ToD_factor (eq. 10 in the ION ITM paper)
ind.channels = [12:467];    % Complex channel estimates for two antennas from both client and access point

end
