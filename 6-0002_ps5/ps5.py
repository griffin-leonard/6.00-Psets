# -*- coding: utf-8 -*-
# Problem Set 5: Modeling Temperature Change
# Name: Griffin Leonard
# Collaborators (discussion): n/a
# Time: 6:30

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE', 
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2011)
TESTING_INTERVAL = range(2011, 2017)

"""
Begin helper code
"""
class Dataset(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Dataset instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def linear_regression(x, y):
    """
    Generate a linear regression models by fitting a to a set of points (x, y).

    Args:
        x: a list of length N, representing the x-coordinates of
            the N sample points
        y: a list of length N, representing the y-coordinates of
            the N sample points

    Returns:
        (m, b): A tuple containing the slope and y-intercept of the regression line,
                which are both floats.
    """
    num = 0 #counter for sumation in numerator of the formula for m
    denom = 0 #counter for sumation in denominator of the formula for m
    #calculate sumations needed in formula for m
    for i in range(len(x)):
        num += (x[i]-np.mean(x))*(y[i]-np.mean(y))
        denom += (x[i]-np.mean(x))**2
    m = num/denom
    b = np.mean(y)-(m*np.mean(x))
    return (m,b)

def evaluate_squared_error(x, y, m, b): 
    '''
    Calculate the squared error for all points in a given regression.

    Args:
        x: a list of length N, representing the x-coordinates of
            the N sample points
        y: a list of length N, representing the y-coordinates of
            the N sample points
        m: The slope of the regression line 
        b: The y-intercept of the regression line


    Returns:
        the total squared error of our regression 
    '''
    return sum([(y[i]-(m*x[i]+b))**2 for i in range(len(x))])

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degs: a list of integers that correspond to the degree of each polynomial 
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    return [np.polyfit(x,y,degs[d]) for d in range(len(degs))]

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model and the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #create a separate plot for each model
    plt.figure()
    for m in models:
        plt.xlabel('Years')
        plt.ylabel('Degrees Celcius')
        plt.plot(x,y,'bo')

        #get the y-values predicted by the model for each x-value
        #used for R^2 score and plotting the best fit curve
        ypred = np.polyval(m,x)
        
        if len(m) == 2:
            plt.title('Yearly Temperature\n(R^2 = '+str(r2_score(y,ypred))\
                +') (SE/slope ='+str(se_over_slope(x,y,ypred,m))+')')
        else:
            plt.title('Yearly Temperature (With best fit curve of degree '\
                +str(len(m)-1)+')\n(R^2 = '+str(r2_score(y,ypred))+')')
        plt.plot(x,ypred,'r-')
        plt.show()

def gen_cities_avg(temp, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        temp: instance of Dataset
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a numpy 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    y = [] 
    for year in years:
        cityTemps = []
        for city in multi_cities:
            dailyTemps = temp.get_yearly_temp(city,year)
            cityTemps.append((sum(dailyTemps)/len(dailyTemps))) #find average yearly temperature for each city
        y.append(sum(cityTemps)/len(cityTemps)) #average the yearly temperatures for each city
    return np.array(y)

def find_interval(x, y, length, has_positive_slope):
    """
    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        has_positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope and j-i = length.

        In the case of a tie, it returns the most recent interval. For example,
        if the intervals (2,5) and (8,11) both have the same slope, (8,11) should
        be returned.

        If such an interval does not exist, returns None
    """
    #create a dictionary mapping slopes to a tuple representing an interval used to get the slope
    slopes = {}
    for i in range(len(x)-length+1):
        slopes[linear_regression(x[i:i+length],y[i:i+length])[0]] = (i,i+length)
        
    #only return an interval if the slope has the correct sign (sign determined by has_positive_slope)
    if has_positive_slope:
        m = max(slopes.keys())
        if m > 0:
            return slopes[m]
    else:
        m = min(slopes.keys())
        if m < 0:
            return slopes[m]
    return None

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return np.mean([(y[n]-estimated[n])**2 for n in range(len(y))])**.5

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    #create a separate plot for each model
    plt.figure()
    for m in models:
        plt.xlabel('Years')
        plt.ylabel('Degrees Celcius')
        plt.plot(x,y,'bo')

        #get the y-values predicted by the model for each x-value
        #used for R^2 score and plotting the best fit curve
        ypred = np.polyval(m,x)
        
        if len(m) == 2:
            plt.title('Yearly Temperature\n(R^2 = '+str(rmse(y,ypred))\
                +') (SE/slope ='+str(se_over_slope(x,y,ypred,m))+')')
        else:
            plt.title('Yearly Temperature (With best fit curve of degree '\
                +str(len(m)-1)+')\n(R^2 = '+str(rmse(y,ypred))+')')
        plt.plot(x,ypred,'r-')
        plt.show()

if __name__ == '__main__':
    data = Dataset('data.csv')
    x = np.array([n for n in range(1961,2017)])
    
#    # Problem 4A
#    y = np.array([data.get_daily_temp('BOSTON',2,12,n) for n in x])
#    evaluate_models_on_training(x,y,generate_models(x,y,[1]))
#    
#    # Problem 4B
#    y = gen_cities_avg(data,['BOSTON'],x)
#    evaluate_models_on_training(x,y,generate_models(x,y,[1]))

#    # Problem 5B
#    y = np.array([sum(data.get_yearly_temp('LOS ANGELES',n))/len(x) for n in x])
#    
#    interval = find_interval(x,y,30,True)
#    x1 = np.array([n for n in range(interval[0],interval[1])])
#    y1 = np.array([sum(data.get_yearly_temp('LOS ANGELES',n))/len(x1) for n in x1])
#    model = generate_models(x1,y1,[1])
#    evaluate_models_on_training(x1,y1,model)
#    
#    interval = find_interval(x,y,30,False)
#    x1 = np.array([n for n in range(interval[0],interval[1])])
#    y1 = np.array([sum(data.get_yearly_temp('LOS ANGELES',n))/len(x1) for n in x1])
#    model = generate_models(x1,y1,[1])
#    evaluate_models_on_training(x1,y1,model)
   
#    # Problem 6B
#    x = np.array([n for n in TRAINING_INTERVAL])
#    y = gen_cities_avg(data,CITIES,x)
#    model = generate_models(x,y,[2,15])
#    evaluate_models_on_training(x,y,model)
#    
#    x = np.array([n for n in TESTING_INTERVAL])
#    y = gen_cities_avg(data,CITIES,x)
#    model = generate_models(x,y,[2,15])
#    evaluate_models_on_testing(x,y,model)


