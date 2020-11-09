import os.path

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import solver
import icons_solver


if __name__ == '__main__':
    for i in range(1, 3):
        for j in range(2, 4):
            icon = "./tests_icons/test1%d_order%d.png" % (i, j)
            background = "./tests_icons/test1%d_bg.png" % i
            if not os.path.exists(icon):
                continue
            print("-"*40)
            print("matching (%s, %s) [%s] and [%s]" % (i, j, icon, background))

            iconGray = cv.imread(icon, cv.IMREAD_GRAYSCALE)
            bgGray = cv.imread(background, cv.IMREAD_GRAYSCALE)
            icons_solver.FeatureMatch(iconGray, bgGray)
