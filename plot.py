from scipy.stats import poisson
import matplotlib.pyplot as plt



def plotting(nodes):
    
    X = []
    for i in range(nodes) :
        X.append(i)
        
        
    lmbda = 2
    #
    # Probability values
    #
    poisson_pd = poisson.pmf(X, lmbda)
    #
    # Plot the probability distribution
    #
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(X, poisson_pd, 'bo', ms=8, label='poisson pmf')
    plt.ylabel("Probability", fontsize="18")
    plt.xlabel("X - No. of Restaurants", fontsize="18")
    plt.title("Poisson Distribution - No. of Restaurants Vs Probability", fontsize="18")
    ax.vlines(X, 0, poisson_pd, colors='b', lw=5, alpha=0.5)
    plt.show()