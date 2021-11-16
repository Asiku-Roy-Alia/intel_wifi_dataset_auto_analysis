% Copyright (C) 2018 Intel Corporation
% SPDX-License-Identifier: BSD-3-Clause

function PlotFTMpositions(measTable, ind)
% This function extracts the client and AP positions and plot them in 2D
% Inputs:
% measTable - a numeric 2D metrix in which each row is an FTM transaction and each column is a variable
% ind - a struct containing fields APpos and GTpos that indicate which columns in measTable contain the AP positions and ground truth positions,
%       respectively

% open figure
figure; 
hAxes=gca;
hold on;

% search in path if the office map file exists
if exist('Office1_40MHz_VenueFile.mat', 'file')
    load('Office1_40MHz_VenueFile.mat')
    imagesc(cfgVenue.xMinMax,cfgVenue.yMinMax,cfgVenue.I,'parent',hAxes)
    set(hAxes,'ydir','normal');
    axis(hAxes,'equal');
end

AP_3D_positions = unique(measTable(:,ind.APpos), 'rows');
client_3D_positions = measTable(:,ind.GTpos);

plot(client_3D_positions(:,1), client_3D_positions(:,2), '.', ...
    AP_3D_positions(:,1), AP_3D_positions(:,2), 'ro','MarkerSize',10,'MarkerFaceColor', 'r', 'parent', hAxes); 
legend('Client positions','AP positions');
title('User and AP positions'); xlabel('Local frame X [m]'); ylabel('Local frame Y [m]');

hold off;
end