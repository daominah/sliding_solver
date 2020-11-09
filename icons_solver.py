import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# twitch params for features matching chinese captcha
def CalcImageEdge3(imgGrey, isPiece=False):
    img1 = np.uint8(imgGrey)

    if isPiece:
        h, w = img1.shape
        img1 = cv.resize(img1, (4*w, 4*h), )
        # img1 = cv.GaussianBlur(img1, (3, 3), 0)
        # _, img1 = cv.threshold(img1, 170, 255, cv.THRESH_BINARY)
        pass
    else:
        img1 = cv.GaussianBlur(img1, (3, 3), 0)
        pass
    # plt.imshow(img1, 'gray'), plt.show()

    scale = 1
    delta = 0
    ddepth = cv.CV_16S
    grad_x = cv.Sobel(img1, ddepth, 1, 0, ksize=3, scale=scale,
                      delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(img1, ddepth, 0, 1, ksize=3, scale=scale,
                      delta=delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    img1 = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    # whoCare, ret = cv.threshold(ret, 85, 255, cv.THRESH_BINARY)

    plt.imshow(img1, 'gray'), plt.show()
    return img1
