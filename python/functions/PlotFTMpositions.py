# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import os
import matplotlib.pyplot as plt
import scipy
    
def PlotFTMpositions(measTable = None,ind = None): 
    # This function extracts the client and AP positions and plot them in 2D
    # Inputs:
    # measTable - a numeric 2D matrix in which each row is an FTM transaction and each column is a variable
    # ind - a struct containing fields APpos and GTpos that indicate which columns in measTable contain the AP positions and ground truth positions,
    #       respectively
    
    # search in path if the office map file exists
    if os.path.exist(str('Office1_40MHz_VenueFile.mat')):
        scipy.io.loadmat('Office1_40MHz_VenueFile.mat')
        imagesc(cfgVenue.xMinMax,cfgVenue.yMinMax,cfgVenue.I,'parent',hAxes)
        set(hAxes,'ydir','normal')
        plt.axis(hAxes,'equal')
    
    AP_3D_positions = unique(measTable(:,ind.APpos),'rows')
    client_3D_positions = measTable(:,ind.GTpos)
    plt.plot(client_3D_positions(:,1),client_3D_positions(:,2),'.',AP_3D_positions(:,1),AP_3D_positions(:,2),'ro','MarkerSize',10,'MarkerFaceColor','r','parent',hAxes)
    plt.legend('Client positions','AP positions')
    plt.title('User and AP positions')
    plt.xlabel('Local frame X [m]')
    plt.ylabel('Local frame Y [m]')

    return
    