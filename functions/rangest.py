def rangest(input_df):
    import pandas as pd 
    import matplotlib.pyplot as plt 
    import numpy as np 
    from functions.estimate_range import estimate_range

    true_range = []
    ml_estimate = []
    range_estimate = [] 

    for i in range(1,102):
        [a,b,c] = estimate_range(i,input_df) 
        true_range.append(b)
        ml_estimate.append(c) 
        range_estimate.append(a) 

    plt.plot(true_range)
    plt.plot(range_estimate)
    plt.plot(ml_estimate)