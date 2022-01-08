# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import os
import matplotlib.pyplot as plt
import scipy
    
def PlotFTMpositions(measTable,office_path,ind): 

    # search in path if the office map file exists
    if os.path.exist(str('Office1_40MHz_VenueFile.mat')):
        scipy.io.loadmat('Office1_40MHz_VenueFile.mat')


    plt.legend('Client positions','AP positions')
    plt.title('User and AP positions')
    plt.xlabel('Local frame X [m]')
    plt.ylabel('Local frame Y [m]')

    return
    