###################################################################
# Filename: plotting.py
# Description: This python script performs all calculations and is
#              plotting all figures that are needed for the .Rnw
#              file (repropack/res/data/Report.Rnw) that is
#              converted to a .tex and a .pdf file and contains a
#              contains a reproducibility report for the 'duckies
#              and fishies' optimization problem described in
#              the 'head_first_data_analysis_chap3' PDF file
#              (repropack/res/data/head_first_data_analysis_chap3.pdf)
# Author: Sabrina Haberl
###################################################################

################
# IMPORTS
################
import pandas
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os
import numpy as np

################
# DICTIONARY
################
# dictionary that defines and includes all constraints needed for the calculation
constraints = {
        "time for ducks" : 400,
        "time for fish" : 300,
        "ducks to produce" : 100,
        "fish to produce" : 100,
        "pellets per duck" : 100,
        "pellets per fish" : 125,
        "pellet supply" : 50000,
        "profit per duck" : 5,
        "profit per fish" : 4,
        "total profit" : 900
    }

################
# FUNCTIONS
################
def objective(x, sign=-1):
    '''
    Attributes: x, sign
    Return values: function
    Description: This function delivers the objective function for the optimization problem solver.
    '''
    return sign*(x[0] * constraints["profit per duck"] + x[1] * constraints["profit per fish"])

def constraint(x):
    '''
    Attributes: x
    Return values: function
    Description: This function delivers a constraint function regarding the pellet supply, that is needed for the optimization problem solver.
    '''
    return constraints["pellet supply"] - (x[0] * constraints["pellets per duck"] + x[1] * constraints["pellets per fish"])

def get_feasible_region():
    '''
    Attributes: none
    Return values: list
    Description: This function calculates the coordinates of the lines that are enclosing the feasible region.
    '''
    data = {}

    # producible amount of ducks and fish according to the pellet supply
    pellets_duck = constraints["pellet supply"] / constraints["pellets per duck"]
    pellets_fish = constraints["pellet supply"] / constraints["pellets per fish"]

    # coordinates for the border of the maximum product mix according to the pellet supply
    data["x_pellets"] = [pellets_fish, 0]
    data["y_pellets"] = [0, pellets_duck]

    # coordinates for the border of the maximum of fish that can be produced according to manufacturing time
    data["x_fish"] = [constraints["time for fish"], constraints["time for fish"]]
    data["y_fish"] = [0, pellets_duck]

    # coordinates for the border of the maximum of ducks that can be produced according to manufacturing time
    data["x_duck"] = [0, pellets_fish]
    data["y_duck"] = [constraints["time for ducks"], constraints["time for ducks"]]   

    return data

def get_maximal_profit():
    '''
    Attributes: none
    Return values: none
    Description: This function calculates the maximum profit under first assumptions.
    '''
    # set constraints
    con = {'type' : 'ineq', 'fun' : constraint}
    
    # set boundaries
    b1 = (0.0, constraints["time for ducks"])
    b2 = (0.0, constraints["time for fish"])
    bnds = (b1, b2)

    # set initial guess
    x0 = [constraints["ducks to produce"], constraints["fish to produce"]]

    # calculate solution of optimization problem
    sol = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = con)

    # update directory with results from optimization
    constraints["ducks to produce"] = round(sol.x[0], 0)
    constraints["fish to produce"] = round(sol.x[1], 0)
    constraints["total profit"] = round(-1*sol.fun, 0)


def get_historical_sales():
    '''
    Attributes: none
    Return values: figure
    Description: This function plots the figure that illustrates the sales of the last months.
    '''
    month = []
    fish = []
    duck = []
    total = []
    x = []
    
    # read source file
    history = pandas.read_csv("../data/historical_sales_data.CSV", sep=";")

    # iterate over rows of the .csv file and append values to seperate lists
    for index, row in history.iterrows():
        month.append(row[0])
        x.append(index)
        fish.append(row[2])
        duck.append(row[3])
        total.append(row[4])

    # plot lines for fish, duck and total sales
    plt.plot(x, fish, label="fish sales")
    plt.plot(x, duck, label="duck sales")
    plt.plot(x, total, label="total sales")
    # plot labels
    plt.xticks(x, month)
    plt.xlabel("Fishes")
    plt.ylabel("Ducks")
    # plot legend
    plt.legend(loc = "upper right")

    plt.show()

def update_plan():
    '''
    Attributes: none
    Return values: none
    Description: This function calculates the maximum profit under updated assumptions.
    '''
    # set constraints
    con = {'type' : 'ineq', 'fun' : constraint}

    # set boundaries
    b_ducks = (0.0, 150.0)
    b_fish = (50.0, constraints["time for fish"])
    bnds = (b_ducks, b_fish)

    # set initial guess
    x0 = [constraints["ducks to produce"], constraints["fish to produce"]]

    # calculate solution of optimization problem
    sol = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = con)

    # update directory with results from optimization
    constraints["ducks to produce"] = round(sol.x[0], 0)
    constraints["fish to produce"] = round(sol.x[1], 0)
    constraints["total profit"] = round(-1*sol.fun, 0)

def plot_maximal_profit():
    '''
    Attributes: none
    Return values: figure
    Description: This function plots the figure that illustrates the result of the optimization using the assumptions at the beginning of the article.
    '''
    # get coordinates of borders for feasible region
    data = get_feasible_region()
    # run optimization with first assumptions
    get_maximal_profit()

    # numpy array with x values for the feasible area
    x = np.arange(0, data["x_fish"][1]+10, 10)
    # calculate y values for the feasible area
    f = ((data["y_pellets"][0] - data["y_pellets"][1])/(data["x_pellets"][0] - data["x_pellets"][1])) * x + ((data["x_pellets"][0]*data["y_pellets"][1]-data["x_pellets"][1]*data["y_pellets"][0])/(data["x_pellets"][0]-data["x_pellets"][1]))
    y = np.minimum(f, data["y_duck"][1])

    # plot line for the maximum pellet supply, fish, ducks
    plt.plot(data["x_pellets"], data["y_pellets"], label="pellet supply")
    plt.plot(data["x_fish"], data["y_fish"], label="number of fish")
    plt.plot(data["x_duck"], data["y_duck"], label="number of ducks")
    # plot dot that marks the maximum profit
    plt.plot(constraints["fish to produce"], constraints["ducks to produce"], "ro", label="maximum profit")
    # plot labels
    plt.xlabel("Fishes")
    plt.ylabel("Ducks")
    # plot legend
    plt.legend(loc = "upper right")
    # plot green coloured area of the feasible region
    plt.fill_between(x, y, where= y<=data["y_duck"][1], color="green", alpha=0.2)

    plt.show()

def plot_update_plan():
    '''
    Attributes: none
    Return values: figure
    Description: This function plots the figure that illustrates the result of the optimization using the updated assumptions of the article.
    '''
    # get coordinates of borders for feasible region
    data = get_feasible_region()
    # run optimization with updated assumptions
    update_plan()

    # numpy array with x values for the feasible area
    x = np.arange(0, data["x_fish"][1]+10, 10)
    # calculate y values for the feasible area
    f = ((data["y_pellets"][0] - data["y_pellets"][1])/(data["x_pellets"][0] - data["x_pellets"][1])) * x + ((data["x_pellets"][0]*data["y_pellets"][1]-data["x_pellets"][1]*data["y_pellets"][0])/(data["x_pellets"][0]-data["x_pellets"][1]))
    y = np.minimum(f, data["y_duck"][1])

    # plot line for the maximum pellet supply, fish, ducks
    plt.plot(data["x_pellets"], data["y_pellets"], label="pellet supply")
    plt.plot(data["x_fish"], data["y_fish"], label="number of fish")
    plt.plot(data["x_duck"], data["y_duck"], label="number of ducks")
    # plot dot that marks the maximum profit
    plt.plot(constraints["fish to produce"], constraints["ducks to produce"], "ro", label="maximum profit")
    # plot labels
    plt.xlabel("Fishes")
    plt.ylabel("Ducks")
    plt.legend(loc = "upper right")
    # plot green coloured area of the feasible region
    plt.fill_between(x, y, where= y<=data["y_duck"][1], color="green", alpha=0.2)

    plt.show()

def print_feasible_result():
    '''
    Attributes: none
    Return values: int array
    Description: This function returns the number of produced ducks and fish and the total profit after the optimization with initial assumptions.
    '''
    get_maximal_profit()
    return [constraints["ducks to produce"], constraints["fish to produce"], constraints["total profit"]]

def print_updated_result():
    '''
    Attributes: none
    Return values: int array
    Description: This function returns the number of produced ducks and fish and the total profit after the optimization with updated assumptions.
    '''
    update_plan()
    return [constraints["ducks to produce"], constraints["fish to produce"], constraints["total profit"]]