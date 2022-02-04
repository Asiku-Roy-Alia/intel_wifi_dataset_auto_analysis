def stats_model(input_df):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np 

    RTT_data = input_df
    nrows = RTT_data.shape[0]

    # Mean and standard deviation of dataset
    meand= 2.429761
    sd =13.484498

    RTT = RTT_data['ToD_factor[m]']
    x_norm = np.random.normal(meand, sd, nrows) 

    text1 ='''
    In statistical analysis, one of the possible analyses that can be conducted is to verify that the data fits a specific distribution, in other words, that the data “matches” a specific theoretical model.
    This kind of analysis is called distribution fitting and consists of finding an interpolating mathematical function that represents the observed phenomenon.
    An example could be when you have a series of observations 𝑥1,𝑥2,𝑥𝑛… and you want to verify if those observations come from a specific population described by a density function 𝑓(𝑥,θ), where θ is a vector of parameters to estimate based on the available data.
    '''
    print(text1) 

    # open figure
    plt.figure(figsize=(12,8))

    # Graphical exploration of the RTT data using histograms
    nbins=50
    plt.hist(RTT,bins=nbins)
    plt.xlabel('RTT')
    plt.ylabel('Count')
    plt.title('Histogram of RTT data(blue) and normally distributed random data')
    plt.hist(x_norm,bins=nbins)
    plt.savefig('graphs/Histogram_RTT_ToD.jpg') 

    print('Another way to display our data is to estimate the probability density function')

    from scipy.stats.kde import gaussian_kde
    from numpy import linspace

    n_samples =int(0.25*nrows )

    # estimate the probability density function (PDF)
    kde = gaussian_kde(x_norm)

    # estimate the probability density function (PDF)
    kded = gaussian_kde(RTT)

    # return evenly spaced numbers over a specified interval
    dist_space = linspace(min(x_norm), max(x_norm), 100) # 100

    # return evenly spaced numbers over a specified interval
    dist_spaced = linspace(min(RTT), max(RTT), 100)

    # plot the results
    plt.figure(figsize=(10,8))
    #plt.subplot(1,2,1)
    plt.plot(dist_spaced, kded(dist_spaced))
    #plt.subplot(1,2,2)
    plt.plot(dist_space, kde(dist_space))
    plt.xlabel('RTT')
    plt.ylabel('PDF')
    plt.title('Probability density functions of RTT (blue) and a random normal dist.')
    plt.savefig('graphs/PDF_RTT.jpg') 

    text2 = '''
    Just by observing those representations is it possible to formulate some ideas about the theoretical models that better fit our data. It is also possible to calculate the empirical distribution function:
    ''' 

    print(text2) 

    plt.figure(figsize=(10,8))
    plt.plot(np.sort(RTT), np.linspace(0, 1, len(RTT)))
    plt.title('Empirical CDF for data')
    plt.plot(np.sort(x_norm), np.linspace(0, 1, len(x_norm)))
    plt.title('Empirical CDF for x_norm')
    plt.xlabel('RTT')
    plt.ylabel('Probabilities')
    plt.savefig('graphs/empirical_probabilities.jpg') 

    text3 = '''
    Another graphical instrument that can come in help is the QQ plot, which shows on the y-axis the quantiles of the observed data VS the theoretical quantiles of the mathematical model.
    With the term quantile, we identify the portion of observations that are below a specific value, the quantile. For example, the 0.75 quantile (or 75%) is the point where 75% of the data (sample) is below this value and 25 % is above.
    When points on the plot tend to lay on the diagonal line, it means that the data(the sample) are fitting the Gaussian model in a “good” way.
    '''

    from scipy import stats
    plt.figure(figsize=(15,8))
    plt.subplot(1,2,1)
    stats.probplot(RTT, plot=plt)
    plt.subplot(1,2,2)
    stats.probplot(x_norm, plot=plt)
    plt.title('QQ plot -RTT(left) and normal dist -right')
    plt.savefig('graphs/QQ-plot.jpg') 

    plt.figure(figsize=(12,8))
    x_wei = np.random.weibull(2, nrows) # A Weibull sample of shape 2and size 500
    plt.hist(x_wei)
    plt.title('Weibull Density function')
    plt.ylabel('Count')
    plt.savefig('graphs/weibull.jpg') 

    text4 = '''
    Parameter estimation
    Once the function that better represents the data is chosen, it is necessary to estimate the parameters that characterize this model based on the available data. Some of the most common methods include a method of moments estimators, least squares, and maximum likelihood estimators. In this introduction we will dig into the following methods:
    the naive method
    the method of moments
    maximum-likelihood
    The naive method is the most basic one and it is quite intuitive: it consists in estimating the parameters of the model by estimating, for example, the average of a sample drawn from a normal distribution with the mean of the sample under study
    ''' 

    # Method of moments

    x_gamma = np.random.gamma(3.5, 0.5, nrows) # simulate a gamma distribution of shape 3.5 and scale (λ) 0.5
    mean_x_gamma = np.mean(x_gamma) # mean of the data
    var_x_gamma = np.var(x_gamma) # variance of the data
    l_est = mean_x_gamma / var_x_gamma # lambda estimation (rate)
    a_est = (mean_x_gamma ** 2) / l_est # alpha estimation
    print('Lambda estimation: {}'.format(l_est))
    print('Alpha estimation: {}'.format(a_est)) 


    # Maximum likelihood estimation
    import statsmodels.api as sm

    # generate data
    x = np.linspace(0,20, len(x_gamma))
    y = 3*x + x_gamma
    ols = sm.OLS(y, x_gamma).fit()
    print(ols.summary())

    #!pip install fitter
    from fitter import Fitter
    f = Fitter(x_gamma, distributions=['gamma', 'dweibull', 'uniform'])
    f.fit()
    f.summary() 





