from colorsys import hsv_to_rgb
import numpy as np

def hsv_color(h,s,v): #h 0-1, s 0-1, v 0-1
    return np.floor(np.array(hsv_to_rgb(h,s,v))*255)
