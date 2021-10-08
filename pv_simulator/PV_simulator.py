import numpy as np

def get_sec(t)->int:
    """
    transform the given datatime in seconds elapsed in the day
    :param t: time in datatime (%m-%d-%Y %H:%M:%S)'s format
    :return: seconds elapsed in the day
    """
    h_min_sec=t.split(" ")[1].split(":")
    return int(h_min_sec[0])*3600 + int(h_min_sec[1])*60 + int(h_min_sec[2])


def gauss(x:float, A:float, mu:float, sigma:float)->float:
    """
    Return the value of a gaussian function in the point x
    :param x: point where the value will be calculated
    :param A: height of the curve's peak
    :param mu: position of the center of the peak
    :param sigma: standard deviation
    :return:
    """
    return A * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

