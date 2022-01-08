% Copyright (C) 2018 Intel Corporation
% SPDX-License-Identifier: BSD-3-Clause

function PlotFTMchannel(measTable, ind, measIndex2Plot)
% This function plots an example channel in the frequency domain
% Inputs:
% measTable - a numeric 2D metrix in which each row is an FTM transaction and each column is a variable
% ind - a struct containing fields APpos and GTpos that indicate which columns in measTable contain the AP positions and ground truth positions,
%       respectively
% measIndex2Plot - an integer in the range [1,29581] (size of the dataset) that chooses which FTM transaction to plot.

Channels_in_freq_domain = measTable(:,ind.channels) % take complex frequency domain channels information from the CSV matrix
% NOTE: The amplitude of the channels is usually not indicative of the SNR/RSSI. The channels were scaled by the hardware.

% The "tone_frequencies" variable below is used to map which baseband frequency, in MHz, corresponds to each of the 114 tones. 
% Note that for 40MHz WiFi, the 3 tones around the DC are never observed

tone_frequencies = 312.5E3*[-58:-2, 2:58] / 1E6 % in MHz 
% reshape the chosen example channel such that the first dimension is the tone
% index, the second is the antenna and the third is the device (client is "side 1", AP is "side 2")
example_channel_in_freq_domain = reshape(Channels_in_freq_domain(measIndex2Plot,:), ...
                                    [114, 2, 2])

% open figure
figure; title('Example channel in frequency domain');
% plot client side amplitude.
subplot(2,2,1); plot(tone_frequencies, 20*log10(abs(example_channel_in_freq_domain(:,:,1))));
title('Channel amplitude at client side'); xlabel('Tone frequency[MHz]'); ylabel('Amplitude[dB]');
% plot AP side amplitude
subplot(2,2,2); plot(tone_frequencies, 20*log10(abs(example_channel_in_freq_domain(:,:,2))));
title('Channel amplitude at AP side'); xlabel('Tone frequency[MHz]'); ylabel('Amplitude[dB]');
% plot client side phase
subplot(2,2,3); plot(tone_frequencies, angle(example_channel_in_freq_domain(:,:,1))); 
title('Channel phase at client side'); xlabel('Tone frequency[MHz]'); ylabel('Phase[rad]');
% plot AP side phase
subplot(2,2,4); plot(tone_frequencies, angle(example_channel_in_freq_domain(:,:,2)));
title('Channel phase at AP side'); xlabel('Tone frequency[MHz]'); ylabel('Phase[rad]');

end