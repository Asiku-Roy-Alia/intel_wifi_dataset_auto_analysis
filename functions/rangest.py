def rangest(input_df):
    from cProfile import label
    import pandas as pd 
    import matplotlib.pyplot as plt 
    import numpy as np 
    from functions.estimate_range import estimate_range
    import random

    rtt_data = input_df
    true_range = []
    ml_estimate = []
    range_estimate = [] 


    for i in range(1,102):
        [a,b,c] = estimate_range(i,input_df) 
        true_range.append(b)
        ml_estimate.append(c) 
        range_estimate.append(a) 

    range_errors_raw = [true_range[i]-range_estimate[i] for i in range(len(true_range))] 
    range_errors_raw=np.array(range_errors_raw)
    ml_range_errors = [true_range[i]-ml_estimate[i] for i in range(len(true_range))]

    est_range_np = np.array(range_estimate)
    mean_range_error  = np.mean(range_errors_raw)
    
    corrected_ranges = est_range_np-mean_range_error 
    range_errors = corrected_ranges-np.array(true_range)

    num_observations = len(true_range) 
    y_rnd = np.random.random_integers(1,50,num_observations)
    z_rnd = np.random.random_integers(1,50,num_observations)

    plt.figure(figsize=(12,8))
    plt.plot(range_errors_raw,label='range errors uncorrected')
    plt.plot(range_errors,label='range errors corrected')
    plt.plot(ml_range_errors, label='ml range errors')
    plt.xlabel('ID')
    plt.ylabel('Range errors')
    plt.title('Range errors of linear and ML models')
    plt.legend()
    plt.savefig('graphs/rangeerrors.jpg')

    plt.figure(figsize=(12,8))
    plt.plot(true_range,'o', label='true range')
    plt.plot(range_estimate,'-', label='range estimate')
    plt.plot(ml_estimate, label='ml range estimate')
    plt.plot(corrected_ranges, label='corrected ranges')
    plt.title('Raw range estimates')
    plt.legend()
    plt.savefig('graphs/Range_estimates.jpg') 

    
    # open figure
    plt.figure(figsize=(12,8))
    # 3D scatter plot with clients
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(y_rnd,z_rnd,true_range, color='g',label='True range');
    ax.scatter3D(y_rnd,z_rnd,ml_estimate, color='y', label='ML range estimate');
    ax.scatter3D(y_rnd,z_rnd,corrected_ranges, color='r',label='Linear range estimate')

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    ax.legend()
    plt.savefig('graphs/3D_scatter_ranges.jpg')  
    

    # open figure
    plt.figure(figsize=(12,8))
    # 3D scatter plot with clients
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(y_rnd,z_rnd,range_errors_raw, color='r',label='Range errors initial');
    ax.scatter3D(y_rnd,z_rnd,range_errors, color='y', label='Linear Range errors biased');
    ax.scatter3D(y_rnd,z_rnd,ml_range_errors, color='b',label='ml range errors')

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    ax.legend()
    plt.savefig('graphs/3D_scatter_range_errors.jpg')  



