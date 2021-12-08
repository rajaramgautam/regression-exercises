import pandas as pd
import math

def plot_residuals(y, yhat):
    residuals = y - yhat
    plt.hlines(0, actual.min(), actual.max(), ls=':')
    plt.scatter(y, residuals)
    plt.ylabel('residual ($y - \hat{y}$)')
    plt.xlabel('actual value ($y$)')
    plt.title('Actual vs Residual')
    plt.show()
    
    
def residuals(y, yhat):
    return y - yhat

def sse(y, yhat):
    return (residuals(y, yhat) **2).sum()

def mse(y, yhat):
    n = y.shape[0]
    return sse(y, yhat) / n

def rmse(y, yhat):
    return math.sqrt(mse(y, yhat))

def ess(y, yhat):
    return ((yhat - y.mean()) ** 2).sum()

def tss(y):
    return ((y - y.mean()) ** 2).sum()

def r2_score(y, yhat):
    return ess(y, yhat) / tss(y)


def regression_errors(y, yhat):
    return pd.Series({
        'sse': sse(y, yhat),
        'ess': ess(y, yhat),
        'tss': tss(y),
        'mse': mse(y, yhat),
        'rmse': rmse(y, yhat),
    })

def regression_errors(actual, predicted):
    return pd.Series({
        'sse': sse(actual, predicted),
        'ess': ess(actual, predicted),
        'tss': tss(actual),
        'mse': mse(actual, predicted),
        'rmse': rmse(actual, predicted),
    })




def baseline_mean_errors(y):
    yhat = y.mean()
    return {
        'sse': sse(y, yhat),
        'mse': mse(y, yhat),
        'rmse': rmse(y, yhat),
    }

def better_than_baseline(y, yhat):
    rmse_baseline = rmse(y, y.mean())
    rmse_model = rmse(y, yhat)
    return rmse_model < rmse_baseline

