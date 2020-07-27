import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

def read_file(file_path, values):
    """
    Loads data from a specified file and returns a list of the
    values requested   

    Parameters
    ----------
    file_path: string, path to the spreadsheet file containing data
    values: list, list of strings each describing a header in the
            loaded file that precedes the requested data
    
    Returns
    -------
    list: a list where each element is a dataset corresponding to the
          header for the requested data in 'values' 
    
    """

    f1 = pd.read_csv(file_path)
    data = []
    for v in values:
        if v in f1:
            data.append(f1[v].tolist())
    return data

def remove_outliers(change_data, to_change, min_val, max_val):
    """
    Removes the outliers in change_data and removes the elements
    at the same indices in each set of data in to_change

    Parameters
    ----------
    change_data: iterable, set of data for which outliers should be
                 removed such that all points of data in change_data
                 are between min_val and max_val inclusive
    to_change: list of iterables, each iterable will have the same
               elements removed as in change_data to ensure that the
               data in change_data and to_change correspond to each other
    min_val: int or float, mininum threshold to not be an outlier
    max_val: int or float, maximum threshold to not be an outlier
    
    Returns
    -------
    list: a list where list[0] is the modified change_data and the other
          elements in the list are the modified iterables from to_change
    """

    change_data = pd.Series(change_data)
    outliers = change_data.between(min_val, max_val)
    change_data = change_data[outliers].tolist()
    
    to_return = []
    to_return.append(change_data)
    for i in to_change:
        i = pd.Series(i)
        i = i[outliers].tolist()
        to_return.append(i)
        
    return to_return

def graph_avg(x, y, pl, opacity, lbf, title=None, x_title=None, y_title=None, label=None, xlim=None, ylim=None):
    """
    Creates and displays a matplotlib scatter plot of y vs. x and also
    draws in error bars for the data x collected at each discrete 
    measurement y.

    Parameters
    ----------
    x: iterable, x-coordinates for values to be plotted
    y: iterable, y-coordinates for values to be plotted
    pl: reference to the already-initialized plot to be used
    opacity: float, opacity of each point in the scatter plot
    lbf: boolean (optional)
         True will graph a line of best fit, False will not
    title: string (optional) title for the plot
    x_title: string (optional) title for the x-axis of the plot
    y_title: string (optional) title for the y-axis of the plot
    label: string (optional) label for the plotted error bars
    x_lim: tuples, minimum and maximum x-values to be displayed
    y_lim: tuples, minimum and maximum x-values to be displayed    
    """
   
    pl.scatter(x, y, marker="o", alpha=opacity)
    d1 = {}
    d1.clear
    for x1, y1 in zip(x, y):
        if x1 not in d1:
            d1[x1] = []
        d1[x1].append(y1)

    x_values = list(d1.keys())
    RSSI_mean = np.array([np.mean(v) for k,v in sorted(d1.items())])
    RSSI_std = np.array([np.std(v) for k,v in sorted(d1.items())])
    pl.errorbar(x_values, RSSI_mean, yerr=RSSI_std, label=label)
    
    pl.set_title(title)
    pl.set_xlabel(x_title)
    pl.set_ylabel(y_title)
    if ylim is not None:
        if len(ylim)==1:
            ylim.append(None)
        pl.set_ylim(ylim[0], ylim[1])
    if xlim is not None:
        if len(xlim)==1:
            xlim.append(None)
        pl.set_xlim(xlim[0], xlim[1])
    
    if lbf:
        x = np.array(x_values)
        best_fit(x, RSSI_mean, pl)
    pl.grid(True)
    pl.legend()

def graph(x, y, pl, opacity, lbf, title=None, x_title=None, y_title=None, xlim=None, ylim=None):
    """
    Creates and displays a matplotlib scatter plot of y vs. x

    Parameters
    ----------
    x: iterable, x-coordinates for values to be plotted
    y: iterable, y-coordinates for values to be plotted
    pl: reference to the already-initialized plot to be used
    opacity: float, opacity of each point in the scatter plot
    lbf: boolean (optional)
         True will graph a line of best fit, False will not
    title: string (optional) title for the plot
    x_title: string (optional) title for the x-axis of the plot
    y_title: string (optional) title for the y-axis of the plot
    label: string (optional) label for the plotted error bars
    x_lim: tuples, minimum and maximum x-values to be displayed
    y_lim: tuples, minimum and maximum x-values to be displayed    
    """

    pl.scatter(x, y, marker="o", alpha=opacity)

    pl.set_title(title)
    pl.set_xlabel(x_title)
    pl.set_ylabel(y_title)
    if ylim is not None:
        if len(ylim)==1:
            ylim.append(None)
        pl.set_ylim(ylim[0], ylim[1])
    if xlim is not None:
        if len(xlim)==1:
            xlim.append(None)
        pl.set_xlim(xlim[0], xlim[1])
    pl.grid(True)
    
    if lbf:
        best_fit(x, y, pl)

def best_fit(x, y, pl):
    """
    Computes and displays the line of best fit and the r^2 value
    for a scatter plot of y vs. x
    
    Utilizes the linregress function from scipy.stats

    Parameters
    ----------
    x: iterable, x-coordinates of plotted values
    y: iterable, y-coordinates of plotted values
    pl: reference to the already-initialized plot to be used
    """
    m, b, r, p, err = stats.linregress(x, y)
    equation = f"y = {round(m,4)}x + {round(b,4)}\nR^2: {round(r**2,8)}"
    pl.plot(x, m*np.array(x)+b, '-r', label=equation)
    pl.legend()


###########################################
### Code to plot RSSI vs. each variable ###
###########################################


### WIND SPEED ###
# Read wind speed data
w_RSSI_1, w_RSSI_2, w_wind = read_file("Desktop/Aggregate.csv",["RSSI-Pi1", "RSSI-Pi2", "Wind Speed"])

# Plot wind speed data scatter plot
fig_w1, ax_w1 = plt.subplots()
fig_w2, ax_w2 = plt.subplots()

graph_avg(w_wind, w_RSSI_1, ax_w1, 1, False, "Pi 1 RSSI Value vs. Wind Speed", "Wind Speed (km/h)", "RSSI Value", "average RSSI", None, None)
graph_avg(w_wind, w_RSSI_2, ax_w2, 1, False, "Pi 2 RSSI Value vs. Wind Speed", "Wind Speed (km/h)", "RSSI Value", "average RSSI", None, None)

# Plot wind speed data with a line of best fit
fig_w1_b, ax_w1_b = plt.subplots()
fig_w2_b, ax_w2_b = plt.subplots()

graph_avg(w_wind, w_RSSI_1, ax_w1_b, 1, True, "Pi 1 RSSI Value vs. Wind Speed with Best Fit", "Wind Speed (km/h)", "RSSI Value", "average RSSI", None, None)
graph_avg(w_wind, w_RSSI_2, ax_w2_b, 1, True, "Pi 2 RSSI Value vs. Wind Speed with Best Fit", "Wind Speed (km/h)", "RSSI Value", "average RSSI", None, None)
### WIND SPEED ###


### BAROMETRIC PRESSURE ###
# Read pressure data
p_r1_1 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi1_1.csv", ["RSSI"])[0]
p_r2_1 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi1_2.csv", ["RSSI"])[0]
p_r3_1 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi1_3.csv", ["RSSI"])[0]
p_r4_1 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi1_4.csv", ["RSSI"])[0]
p_r5_1 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi1_5.csv", ["RSSI"])[0]

p1_2, p_r1_2 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi2_1.csv", ["PRESSURE","RSSI"])
p2_2, p_r2_2 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi2_2.csv", ["PRESSURE","RSSI"])
p3_2, p_r3_2 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi2_3.csv", ["PRESSURE","RSSI"])
p4_2, p_r4_2 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi2_4.csv", ["PRESSURE","RSSI"])
p5_2, p_r5_2 = read_file("Desktop/Lee_Audrey_CollectedData/Pressure/pres_pi2_5.csv", ["PRESSURE","RSSI"])

p = p1_2 + p2_2 + p3_2 + p4_2 + p5_2
p_r_1 = p_r1_1 + p_r2_1 + p_r3_1 + p_r4_1 + p_r5_1
p_r_2 = p_r1_2 + p_r2_2 + p_r3_2 + p_r4_2 + p_r5_2

# Plot pressure data scatter plot
fig_p1, ax_p1 = plt.subplots()
fig_p2, ax_p2 = plt.subplots()

graph(p, p_r_1, ax_p1, 0.25, False, "Pi 1 RSSI Value vs. Barometric Pressure", "Barometric Pressure (Pascals/Pa)", "RSSI Value", (63000, 102000), (-50, -20))
graph(p, p_r_2, ax_p2, 0.25, False, "Pi 2 RSSI Value vs. Barometric Pressure", "Barometric Pressure (Pascals/Pa)", "RSSI Value", (63000, 102000), (-50, -20))

# Remove outliers from the pressure data
p, p_r_1, p_r_2 = remove_outliers(p, [p_r_1, p_r_2], 63205, 101000)
p_r_1, p, p_r_2 = remove_outliers(p_r_1, [p, p_r_2], -50, -35)
p_r_2, p, p_r_1 = remove_outliers(p_r_2, [p, p_r_1], -50, -35)

# Plot pressure data with a line of best fit
fig_p1_b, ax_p1_b = plt.subplots()
fig_p2_b, ax_p2_b = plt.subplots()

graph(p, p_r_1, ax_p1_b, 0.25, True, "Pi 1 RSSI Value vs. Barometric Pressure with Best Fit", "Barometric Pressure (Pascals/Pa)", "RSSI Value", (63000, 102000), (-50, -20))
graph(p, p_r_2, ax_p2_b, 0.25, True, "Pi 2 RSSI Value vs. Barometric Pressure with Best Fit", "Barometric Pressure (Pascals/Pa)", "RSSI Value", (63000, 102000), (-50, -20))
### BAROMETRIC PRESSURE ###


### RELATIVE HUMIDITY ###
# Read humidity data
h_r1_1 = read_file("Desktop/Lee_Audrey_CollectedData/Humidity/hum_pi1_1.csv", ["RSSI"])[0]
h_r2_1 = read_file("Desktop/Lee_Audrey_CollectedData/Humidity/hum_pi1_2.csv", ["RSSI"])[0]
h_r3_1 = read_file("Desktop/Lee_Audrey_CollectedData/Humidity/hum_pi1_3.csv", ["RSSI"])[0]

h1_2, h_r1_2 = read_file("Desktop/Lee_Audrey_CollectedData/Humidity/hum_pi2_1.csv", ["HUMIDITY","RSSI"])
h2_2, h_r2_2 = read_file("Desktop/Lee_Audrey_CollectedData/Humidity/hum_pi2_2.csv", ["HUMIDITY","RSSI"])
h3_2, h_r3_2 = read_file("Desktop/Lee_Audrey_CollectedData/Humidity/hum_pi2_3.csv", ["HUMIDITY","RSSI"])

h = h1_2 + h2_2 + h3_2
h_r_1 = h_r1_1 + h_r2_1 + h_r3_1
h_r_2 = h_r1_2 + h_r2_2 + h_r3_2

# Plot humidity data scatter plot
fig_h1, ax_h1 = plt.subplots()
fig_h2, ax_h2 = plt.subplots()

graph(h, h_r_1, ax_h1, 0.25, False, "Pi 1 RSSI Value vs. Relative Humidity", "Relative Humidity (%)", "RSSI Value", None, None)
graph(h, h_r_2, ax_h2, 0.25, False, "Pi 2 RSSI Value vs. Relative Humidity", "Relative Humidity (%)", "RSSI Value", None, None)

# Remove outliers from the humidity data
h, h_r_1, h_r_2 = remove_outliers(h, [h_r_1, h_r_2], 30, 85)
h_r_1, h, h_r_2 = remove_outliers(h_r_1, [h, h_r_2], -40, -15)
h_r_2, h, h_r_1 = remove_outliers(h_r_2, [h, h_r_1], -40, -15)

# Plot humidity data with a line of best fit
fig_h1_b, ax_h1_b = plt.subplots()
fig_h2_b, ax_h2_b = plt.subplots()

graph(h, h_r_1, ax_h1_b, 0.25, True, "Pi 1 RSSI Value vs. Relative Humidity with Best Fit", "Relative Humidity (%)", "RSSI Value", None, None)
graph(h, h_r_2, ax_h2_b, 0.25, True, "Pi 2 RSSI Value vs. Relative Humidity with Best Fit", "Relative Humidity (%)", "RSSI Value", None, None)
### RELATIVE HUMIDITY ###


### AMBIENT TEMPERATURE ###
# Read temperature data
t_r1_1 = read_file("Desktop/Lee_Audrey_CollectedData/Temperature/temp_pi1_1.csv", ["RSSI"])[0]
t_r2_1 = read_file("Desktop/Lee_Audrey_CollectedData/Temperature/temp_pi1_2.csv", ["RSSI"])[0]
t_r3_1 = read_file("Desktop/Lee_Audrey_CollectedData/Temperature/temp_pi1_3.csv", ["RSSI"])[0]

t1_2, t_r1_2 = read_file("Desktop/Lee_Audrey_CollectedData/Temperature/temp_pi2_1.csv", ["TEMP","RSSI"])
t2_2, t_r2_2 = read_file("Desktop/Lee_Audrey_CollectedData/Temperature/temp_pi2_2.csv", ["TEMP","RSSI"])
t3_2, t_r3_2 = read_file("Desktop/Lee_Audrey_CollectedData/Temperature/temp_pi2_3.csv", ["TEMP","RSSI"])

t = t1_2 + t2_2 + t3_2
t_r_1 = t_r1_1 + t_r2_1 + t_r3_1
t_r_2 = t_r1_2 + t_r2_2 + t_r3_2

# Plot temperature data scatter plot
fig_t1, ax_t1 = plt.subplots()
fig_t2, ax_t2 = plt.subplots()

graph(t, t_r_1, ax_t1, 0.25, False, "Pi 1 RSSI Value vs. Ambient Temperature", "Ambient Temperature (°C)", "RSSI Value", None, None)
graph(t, t_r_2, ax_t2, 0.25, False, "Pi 2 RSSI Value vs. Ambient Temperature", "Ambient Temperature (°C)", "RSSI Value", None, None)

# Remove outliers from the temperature data
t, t_r_1, t_r_2 = remove_outliers(t, [t_r_1, t_r_2], -10, 40)
t_r_1, t, t_r_2 = remove_outliers(t_r_1, [t, t_r_2], -70, -10)
t_r_2, t, t_r_1 = remove_outliers(t_r_2, [t, t_r_1], -70, -10)

# Plot humidity data with a line of best fit
fig_t1_b, ax_t1_b = plt.subplots()
fig_t2_b, ax_t2_b = plt.subplots()

graph(t, t_r_1, ax_t1_b, 0.25, True, "Pi 1 RSSI Value vs. Ambient Temperature", "Ambient Temperature (°C)", "RSSI Value", None, None)
graph(t, t_r_2, ax_t2_b, 0.25, True, "Pi 2 RSSI Value vs. Ambient Temperature", "Ambient Temperature (°C)", "RSSI Value", None, None)
### AMBIENT TEMPERATURE ###