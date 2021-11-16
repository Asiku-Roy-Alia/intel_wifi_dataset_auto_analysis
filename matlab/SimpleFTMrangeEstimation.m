% Copyright (C) 2018 Intel Corporation
% SPDX-License-Identifier: BSD-3-Clause

function SimpleFTMrangeEstimation(measTable, ind)
% This function demonstrates how to use the data to estimate the ranges between AP and client.
% It then plots a CDF of the resulting range errors.
% Here, we perform a very simple Time of Arrival (ToA) estimation procedure from a single antenna for both client and AP.
% The channel is first transformed from frequency-domain to time-domain using inverse fast Fourier transform (IFFT). The estimated ToA is then the location
% of the highest power peak in the time domain channel.
% In "A Machine Learning Approach for Wi-Fi RTT Ranging" (ION ITM 2019), a maximum-likelihood and neural network estimators are used intead.
% As in the ION paper, APs numbered [1:3] and [7:12] are used for calibrating the algorithm and the performance is measured on measurements from APs
% numbered [4:6].
% Inputs:
% measTable - a numeric 2D metrix in which each row is an FTM transaction and each column is a variable
% ind - a struct containing fields GTrange, ToDfactor and channels that indicate which columns in measTable contain the ground truth ranges, ToD
% factors and frequency domain channel estimates, respectively. It should also contain a field APnum that indicated, for each FTM measurement, with
% which AP that measurement was performed.

% reshape the entire channels matrix such that the first dimension is the measurement index, seconds is tone
% index, the third is the antenna and the fourth is the device (client is "side 1", AP is "side 2")
channels_in_freq_domain = reshape(measTable(:,ind.channels), ...
                                    [], 114, 2, 2);

num_channels = size(measTable,1); % number of measurements

% Take frequency domain channel from the first antenna
channels_freq_domain  = channels_in_freq_domain(:,:,1,:); % antenna 1 channels, for both AP and client

% Add 3 DC tones and guard subcarriers for 40MHz Wi-Fi
channels_freq_domain_pad = cat(2, ...
                                zeros(num_channels, 6,2), ... % guard subcarriers
                                channels_freq_domain(:,1:57,:), ...
                                zeros(num_channels, 3,2), ... % DC subcarriers
                                channels_freq_domain(:, 58:end,:), ...
                                zeros(num_channels, 5,2)); % guard subcarriers                
                        
% Transform channels to time domain
channel_time_domain = ifft(ifftshift(channels_freq_domain_pad,2),[],2);

% Circular shift of the resulting channel by 10 samples. This is done in order to simplify the peak finding, since sometimes the maximum of the peak
% is located on the negative side (i.e. the ToA can be slightly negative, but not large positive)
% This extra circular shift is later corrected for below.
N_samples_to_shift = 10; % integer number of samples to circular shift
channel_time_domain_circ_shifted = circshift(channel_time_domain, N_samples_to_shift, 2);
                      
% Estimate the ToAs by finding the highest peak in the time domain, in terms of samples
[~, est_ToA_index_client] = max(abs(channel_time_domain_circ_shifted(:,:,1)),[],2);
[~, est_ToA_index_AP]     = max(abs(channel_time_domain_circ_shifted(:,:,2)),[],2);

% Correct ToA indexes by -N_samples_to_shift
est_ToA_index_client    = est_ToA_index_client - N_samples_to_shift;
est_ToA_index_AP        = est_ToA_index_AP - N_samples_to_shift;

% Translate the sample index to time in seconds
% The channels are sampled at 40MHz. The entire symbol is 3.2usec length.
delta_time_per_sample = 1/40e6; % time difference between each two samples (sec)
est_ToA_client = (est_ToA_index_client - 1)*delta_time_per_sample;  % estimated client ToA in seconds
est_ToA_AP     = (est_ToA_index_AP - 1)*delta_time_per_sample;      % estimated AP ToA in seconds

% Calculate estimated range and range error
ToD_factor = measTable(:,ind.ToDfactor); % in meters
est_range = ToD_factor + (est_ToA_client + est_ToA_AP)*3e8/2; % estimated range [m]
GT_range = measTable(:, ind.GTrange); % ground truth range for this measurement [m]
range_error = est_range - GT_range; % estimated range error [m]

% Use APs numbered [1:3] and [7:12] to calibrate a constant correction to the range estimate.
% Constant range bias can be caused e.g. by multipath or hardware calibration.
TestInd = measTable(:,ind.APnum) == 4 | measTable(:,ind.APnum) == 5 | measTable(:,ind.APnum) == 6; % measurements of the test set
TrainInd = ~TestInd; % any measurement that's not in the test set, consider as train set.
bias_estimate = median(range_error(TrainInd)); % estimated average bias of the algorithm, according to the train set
corrected_range_errors = range_error - bias_estimate; % post-fit range errors

% Plot CDF of range errors on the test set only
final_range_errors_on_test_set = corrected_range_errors(TestInd);
figure; ecdf(abs(final_range_errors_on_test_set));
title(['Estimated range error on test set: using ifft on one antenna']);
xlim([0,20]); xlabel('range error [m]');
end